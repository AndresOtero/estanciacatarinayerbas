#!/usr/bin/env python3
"""Genera index.html (estatico, sin JavaScript) a partir de products.json.

Uso:  python3 build.py
Las imagenes se buscan en img/<slug>.<jpg|jpeg|png|webp>. Si no existe
ninguna, la tarjeta se genera directamente con el placeholder.
"""

import html
import json
import re
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).parent
IMG_DIR = RAIZ / "img"
EXTENSIONES = (".jpg", ".jpeg", ".png", ".webp")

# Ordenadas por longitud DESC para que "REI VERDE" no se confunda con "REI".
MARCAS_CONOCIDAS = sorted(
    [
        "REI VERDE",
        "Emperatriz del Monte",
        "CANARIAS",
        "CENTENARIA",
        "PINDARÉ",
        "VERDECITA",
        "BALDO",
        "ESMERALDA",
        "LATINA",
        "SARA",
        "BARÃO",
        "CONTIGO",
        "CÓSMICO",
    ],
    key=len,
    reverse=True,
)


def sin_tildes(texto):
    descompuesto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in descompuesto if unicodedata.category(c) != "Mn")


def slug(nombre):
    base = sin_tildes(nombre).lower()
    return re.sub(r"^-|-$", "", re.sub(r"[^a-z0-9]+", "-", base))


def obtener_marca(nombre):
    for marca in MARCAS_CONOCIDAS:
        if nombre.startswith(marca + " ") or nombre == marca:
            return marca
    return nombre.split(" ")[0]


def formato_precio(n):
    """10500 -> '10.500' (separador de miles rioplatense)."""
    return f"{n:,}".replace(",", ".")


def buscar_imagen(s):
    for ext in EXTENSIONES:
        if (IMG_DIR / f"{s}{ext}").is_file():
            return f"img/{s}{ext}"
    return None


def tarjeta(producto):
    nombre = producto["nombre"]
    nombre_esc = html.escape(nombre)
    ruta = buscar_imagen(slug(nombre))

    if ruta:
        medio = (
            f'<img src="{html.escape(ruta)}" alt="{nombre_esc}" '
            f'width="400" height="400" loading="lazy" decoding="async" />'
        )
    else:
        medio = f'<div class="no-img">📷 {nombre_esc}</div>'

    return f"""                <article class="product-card">
                    <div class="product-image">{medio}</div>
                    <h3 class="product-name">{nombre_esc}</h3>
                    <p class="product-price">{formato_precio(producto["precio"])}</p>
                    <p class="product-weight">{html.escape(producto["peso"])}</p>
                </article>"""


def main():
    productos = json.loads((RAIZ / "products.json").read_text(encoding="utf-8"))

    agrupados = {}
    for p in productos:
        agrupados.setdefault(obtener_marca(p["nombre"]), []).append(p)

    marcas = sorted(agrupados, key=lambda m: sin_tildes(m).upper())

    secciones = []
    for marca in marcas:
        tarjetas = "\n".join(tarjeta(p) for p in agrupados[marca])
        secciones.append(
            f"""    <section class="brand-section" id="{slug(marca)}">
        <h2 class="brand-title">{html.escape(marca)}</h2>
        <div class="product-grid">
{tarjetas}
        </div>
    </section>"""
        )

    plantilla = (RAIZ / "template.html").read_text(encoding="utf-8")
    salida = plantilla.replace("<!--CONTENIDO-->", "\n\n".join(secciones))
    (RAIZ / "index.html").write_text(salida, encoding="utf-8")

    con_img = sum(1 for p in productos if buscar_imagen(slug(p["nombre"])))
    print(f"index.html generado: {len(productos)} productos, {len(marcas)} marcas.")
    print(f"Imagenes encontradas: {con_img}/{len(productos)}")


if __name__ == "__main__":
    main()
