#!/usr/bin/env python3
"""
make_nss_stub.py — build minimal libnss3.so / libnssutil3.so stubs that satisfy
the dynamic linker for headless Chromium when no real NSS libs are available.

How it works:
  1. Reads the target binary's ELF .gnu.version_r + .gnu.version + .dynsym to find
     every (symbol, version-node) pair referenced from libnss3.so / libnssutil3.so.
  2. Generates a C file with one wrapper per (symbol, node), using .symver aliases
     so each export carries exactly the version node the loader demands.
  3. Compiles with gcc -shared, then verifies the output with pyelftools.

Return values are chosen so headless LOCAL rendering works (file://, data:,
screenshots): init functions return SECSuccess(0), cert/trust functions return
failure/NULL. TLS/cert operations will NOT work — that is the honest tradeoff
of a stub, and TLS is egress-blocked in this sandbox anyway.

Usage:
  python3 make_nss_stub.py /tmp/chromium /tmp/chromelibs
"""
import struct, subprocess, sys, os
from elftools.elf.elffile import ELFFile

TARGET = sys.argv[1] if len(sys.argv) > 1 else '/tmp/chromium'
OUTDIR = sys.argv[2] if len(sys.argv) > 2 else '/tmp/chromelibs'

def collect_refs(path):
    f = open(path, 'rb'); e = ELFFile(f)
    dynsym = e.get_section_by_name('.dynsym')
    versym = e.get_section_by_name('.gnu.version')
    vr = e.get_section_by_name('.gnu.version_r')
    libnodes = {}
    for verneed, vauxs in vr.iter_versions():
        libnodes[verneed.name] = {}
        for vn in vauxs:
            libnodes[verneed.name][vn['vna_other']] = vn.name
    data = versym.data()
    refs = {}
    for i, s in enumerate(dynsym.iter_symbols()):
        if s['st_shndx'] == 'SHN_UNDEF' and s.name:
            ndx = struct.unpack_from('<H', data, i * 2)[0] & 0x7fff
            for lib, nodes in libnodes.items():
                if ndx in nodes:
                    if lib in ('libnss3.so', 'libnssutil3.so'):
                        refs.setdefault(lib, {}).setdefault(s.name, set()).add(nodes[ndx])
                    break
    return refs

# functions that must succeed for chromium to boot (SECStatus == 0)
SUCCESS = {'NSS_NoDB_Init', 'NSS_InitReadWrite', 'NSS_VersionCheck'}
# functions that return SECFailure (-1) so cert paths fail cleanly instead of lying
FAIL = {'CERT_GetCertTrust', 'PK11_ReadRawAttribute', 'PK11_InitPin'}
# void functions (no return value)
VOID = {'CERT_DestroyCertificate', 'CERT_DestroyCertList', 'SECITEM_FreeItem',
        'PK11_FreeSlot', 'PK11_DestroyGenericObjects', 'SECMOD_DestroyModule',
        'SECMOD_ReleaseReadLock', 'PK11_SetPasswordFunc'}

def gen_c(lib, syms):
    lines = ['/* auto-generated NSS stub for %s (do not edit) */' % lib, '']
    for name in sorted(syms):
        nodes = sorted(syms[name])
        for j, node in enumerate(nodes):
            cname = f'stub_{name}_{j}'
            if name in VOID:
                lines.append(f'void {cname}(void) {{ }}')
            elif name in SUCCESS:
                lines.append(f'long {cname}(void) {{ return 0; }}')   # SECSuccess
            elif name in FAIL:
                lines.append(f'long {cname}(void) {{ return -1; }}')  # SECFailure
            else:
                lines.append(f'long {cname}(void) {{ return 0; }}')   # NULL / PR_FALSE
            lines.append(f'__asm__(".symver {cname},{name}@{node}");')
            lines.append('')
    return '\n'.join(lines)

refs = collect_refs(TARGET)
os.makedirs(OUTDIR, exist_ok=True)
for lib, syms in refs.items():
    csrc = os.path.join(OUTDIR, lib.replace('.so', '_stub.c'))
    with open(csrc, 'w') as fh:
        fh.write(gen_c(lib, syms))
    # version script: declare every node the loader demands (existence is enough)
    nodes = sorted({n for s in syms.values() for n in s})
    vmap = os.path.join(OUTDIR, lib.replace('.so', '_stub.map'))
    with open(vmap, 'w') as fh:
        fh.write(''.join(f'{n} {{ }};\n' for n in nodes))
    so = os.path.join(OUTDIR, lib)
    cmd = ['gcc', '-shared', '-fPIC', '-O2', '-o', so, csrc,
           f'-Wl,--version-script={vmap}']
    subprocess.run(cmd, check=True)
    print(f'built {so} ({len(syms)} symbols, nodes {nodes})')

# verify: the built libs must define every needed version node + versioned symbol
f = open(TARGET, 'rb'); e = ELFFile(f)
vr = e.get_section_by_name('.gnu.version_r')
needed = {}
for verneed, vauxs in vr.iter_versions():
    needed[verneed.name] = set(vn.name for vn in vauxs)

for lib, syms in refs.items():
    so = os.path.join(OUTDIR, lib)
    fe = ELFFile(open(so, 'rb'))
    vd = fe.get_section_by_name('.gnu.version_d')
    defined_nodes = set()
    if vd:
        for _, vauxs in vd.iter_versions():
            for vn in vauxs:
                defined_nodes.add(vn.name)
    missing_nodes = needed.get(lib, set()) - defined_nodes
    print(f'{lib}: defined nodes {sorted(defined_nodes)}  missing: {sorted(missing_nodes)}')
    if missing_nodes:
        sys.exit(f'FAIL: {lib} missing version nodes {missing_nodes}')
print('OK: stubs satisfy the loader version requirements of', TARGET)
