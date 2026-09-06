#!/usr/bin/env python3
"""Servidor local para previsualizar el sitio antes de publicarlo.

Uso:  python3 scripts/serve.py [puerto]      (por defecto, 8000)

Sirve la raiz del repositorio y regenera index.html en cada carga de la
pagina: edita data/products.json o templates/template.html, refresca el
navegador y ves el cambio. No hace falta ejecutar build.py a mano
mientras el servidor esta corriendo.
"""

import contextlib
import io
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import build

# Se sirve la raiz del repositorio (donde build.py escribe index.html),
# no el directorio scripts/ en el que vive este archivo.
RAIZ = Path(__file__).resolve().parent.parent


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            try:
                # build.main() imprime un resumen; lo silenciamos por pedido.
                with contextlib.redirect_stdout(io.StringIO()):
                    build.main()
            except Exception as exc:
                self.send_error(500, f"Error al generar index.html: {exc}")
                return
        super().do_GET()

    def end_headers(self):
        # Evita que el navegador cachee una version vieja de la pagina.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def main():
    puerto = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    handler = partial(Handler, directory=str(RAIZ))
    with ThreadingHTTPServer(("0.0.0.0", puerto), handler) as servidor:
        print(f"Sirviendo en http://localhost:{puerto}/   (Ctrl+C para salir)")
        print("index.html se regenera en cada recarga.")
        try:
            servidor.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")


if __name__ == "__main__":
    main()
