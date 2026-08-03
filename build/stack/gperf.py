#!/usr/bin/env python3
"""Minimal gperf-compatible generator for fontconfig's fcobjshash.h.

Real gperf emits a perfect-hash lookup. We emit a linear-scan table which is
semantically identical and more than fast enough for ~60 fontconfig objects.
Handles the two invocation shapes fontconfig's meson build uses:
  1) gperf -L ANSI-C <file>                    -> stdout test snippet (uses size_t)
  2) gperf --pic -m 100 <input> --output-file <output>
"""
import re
import sys


def emit_test_snippet():
    # Must compile after:  const char * in_word_set(const char *, size_t);
    sys.stdout.write(
        "const char * in_word_set(const char *str, size_t len)\n"
        "{ (void)str; (void)len; return (const char *)0; }\n"
    )
    return 0


def main():
    args = sys.argv[1:]
    if "-L" in args:
        return emit_test_snippet()

    inp = None
    out = None
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--output-file":
            i += 1
            out = args[i]
        elif a == "-m":
            i += 1  # skip its value
        elif a.startswith("-"):
            pass  # --pic and friends: ignored
        else:
            inp = a
        i += 1
    if not inp or not out:
        sys.stderr.write("fake-gperf: need input and --output-file\n")
        return 1

    spec = open(inp, encoding="utf8", errors="replace").read()

    # declaration block: everything before the first %%
    parts = spec.split("%%", 1)
    decls = parts[0]
    body = parts[1] if len(parts) > 1 else ""

    # struct definition from the declaration block
    m = re.search(r"struct\s+FcObjectTypeInfo\s*\{[^}]*\};", decls)
    struct_def = (
        "struct FcObjectTypeInfo {\n\tint name;\n\tint id;\n};"
        if not m
        else m.group(0).replace("\n\t", "\n\t")
    )

    # keyword table entries: lines like "family",FC_FAMILY_OBJECT
    entries = []
    for line in body.splitlines():
        line = line.strip()
        mm = re.match(r'^"((?:[^"\\]|\\.)*)"\s*,\s*([A-Za-z0-9_]+)\s*$', line)
        if mm:
            key = mm.group(1).replace('\\"', '"')
            entries.append((key, mm.group(2)))

    if not entries:
        sys.stderr.write("fake-gperf: no keyword entries found\n")
        return 1

    # build string pool + offsets
    pool = ""
    offsets = []
    for key, _ in entries:
        offsets.append(len(pool))
        pool += key + "\0"

    lines = []
    lines.append("/* ANSI-C code produced by gperf (compatible generator) */")
    lines.append("#include <string.h>")
    lines.append("")
    lines.append(struct_def)
    lines.append("")
    n = len(entries)
    lines.append(f"/* maximum key range = {max(len(k) for k,_ in entries)}, duplicates = 0 */")
    lines.append("")
    # string pool as concatenated C string literals
    pool_chunks = [pool[i : i + 60] for i in range(0, len(pool), 60)] or [""]
    lines.append("static const char FcObjectTypeNamePool[] =")
    for c in pool_chunks:
        c_esc = c.replace('"', '\\"').replace("\0", "\\0")
        lines.append(f'  "{c_esc}"')
    lines[-1] += ";"
    lines.append("")
    lines.append("static const struct FcObjectTypeInfo FcObjectType_wordlist[] =")
    lines.append("  {")
    for (key, val), off in zip(entries, offsets):
        lines.append(f"    {{{off}, {val}}},  /* \"{key}\" */")
    lines.append("  };")
    lines.append("")
    lines.append("const struct FcObjectTypeInfo *")
    lines.append("FcObjectTypeLookup (register const char *str, register FC_GPERF_SIZE_T len)")
    lines.append("{")
    lines.append("  unsigned int i;")
    lines.append("  const char *s;")
    lines.append("  for (i = 0; i < sizeof (FcObjectType_wordlist) / sizeof (FcObjectType_wordlist[0]); i++)")
    lines.append("    {")
    lines.append("      s = FcObjectTypeNamePool + FcObjectType_wordlist[i].name;")
    lines.append("      if (strncmp (str, s, len) == 0 && s[len] == '\\0')")
    lines.append("        return &FcObjectType_wordlist[i];")
    lines.append("    }")
    lines.append("  return (const struct FcObjectTypeInfo *) 0;")
    lines.append("}")
    lines.append("")
    lines.append("unsigned int")
    lines.append("FcObjectTypeHash (register const char *str, register FC_GPERF_SIZE_T len)")
    lines.append("{")
    lines.append("  unsigned int h = 5381;")
    lines.append("  while (len-- != 0)")
    lines.append("    h = h * 33 + (unsigned char) *str++;")
    lines.append("  return h;")
    lines.append("}")
    lines.append("")

    with open(out, "w", encoding="utf8") as f:
        f.write("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
