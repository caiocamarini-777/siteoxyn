"""Servidor local com URLs limpas (igual ao Vercel com cleanUrls).
Uso (na raiz do repo): python3 scripts/dev-server.py [porta]
"""
import http.server, os, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 4173

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)
    def send_head(self):
        path = self.path.split("?", 1)[0].split("#", 1)[0]
        local = ROOT / path.lstrip("/")
        if path != "/" and not local.exists() and (ROOT / (path.lstrip("/") + ".html")).exists():
            self.path = path + ".html"
        return super().send_head()
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

print(f"Oxyn dev server: http://localhost:{PORT}")
http.server.ThreadingHTTPServer(("", PORT), Handler).serve_forever()
