#!/usr/bin/env python3
"""VIKAAS preview server — static files + HTTP Range support (fixes <video> streaming
   that python's stock http.server can't do; Chrome/Safari need 206 Partial Content)."""
import http.server, os, re, sys, mimetypes

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 4173

class RangeHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def end_headers(self):
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def send_head(self):
        rng = self.headers.get('Range')
        if not rng:
            return super().send_head()
        path = self.translate_path(self.path)
        if not os.path.isfile(path):
            return super().send_head()
        m = re.match(r'bytes=(\d*)-(\d*)', rng)
        if not m:
            self.send_error(416); return None
        size = os.path.getsize(path)
        start = int(m.group(1)) if m.group(1) else 0
        end = int(m.group(2)) if m.group(2) else size - 1
        if m.group(1) == '':  # bytes=-N suffix form
            end = size - 1; start = max(0, size - int(m.group(2)))
        if start >= size:
            self.send_error(416); return None
        end = min(end, size - 1)
        ctype = self.guess_type(path)
        self.send_response(206)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length', str(end - start + 1))
        self.end_headers()
        f = open(path, 'rb'); f.seek(start)
        remaining = end - start + 1
        class Chunk:
            def __init__(self, fh, n): self.fh, self.n = fh, n
            def read(self, amt=-1):
                if self.n <= 0: return b''
                if amt < 0 or amt > self.n: amt = self.n
                data = self.fh.read(amt); self.n -= len(data)
                if self.n <= 0: self.fh.close()
                return data
            def close(self): self.fh.close()
        return Chunk(f, remaining)

    def log_message(self, fmt, *args):
        sys.stderr.write('%s - %s\n' % (self.address_string(), fmt % args))

if __name__ == '__main__':
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    srv = http.server.ThreadingHTTPServer(('0.0.0.0', PORT), RangeHandler)
    print(f'serving {ROOT} on 0.0.0.0:{PORT} (Range-capable)')
    srv.serve_forever()
