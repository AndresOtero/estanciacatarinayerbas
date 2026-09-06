#!/usr/bin/env python3
"""Genera index.html (estatico, sin JavaScript) a partir de products.json.

Uso:  python3 scripts/build.py   (desde la raiz del repositorio)

Lee data/products.json, lo inserta en templates/template.html y escribe
index.html en la raiz, que es de donde lo publica GitHub Pages.

Las imagenes se buscan en img/<slug>.<jpg|jpeg|png|webp>. Si no existe
ninguna, la tarjeta se genera directamente con el placeholder.
"""

import html
import json
import re
import unicodedata
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuracion
# ---------------------------------------------------------------------------

# El script vive en scripts/, asi que la raiz del repositorio es un nivel
# mas arriba. Las rutas son absolutas para poder ejecutarlo desde cualquier
# directorio de trabajo.
RAIZ = Path(__file__).resolve().parent.parent
PRODUCTOS_JSON = RAIZ / "data" / "products.json"
PLANTILLA_HTML = RAIZ / "templates" / "template.html"
SALIDA_HTML = RAIZ / "index.html"
IMG_DIR = RAIZ / "img"

EXTENSIONES = (".jpg", ".jpeg", ".png", ".webp")
MARCADOR_CONTENIDO = "<!--CONTENIDO-->"

# Marcas cuyo nombre no coincide con la primera palabra del producto, o que
# tienen mas de una palabra. Se listan alfabeticamente para mantenerlas y se
# ordenan por longitud DESC al cargar, para que "REI VERDE" no se confunda
# con "REI".
MARCAS_CONOCIDAS = sorted(
    [
        "BALDO",
        "BARÃO",
        "CANARIAS",
        "CENTENARIA",
        "CONTIGO",
        "CÓSMICO",
        "Emperatriz del Monte",
        "ESMERALDA",
        "LATINA",
        "PINDARÉ",
        "REI VERDE",
        "SARA",
        "VERDECITA",
    ],
    key=len,
    reverse=True,
)


# ---------------------------------------------------------------------------
# Utilidades de texto
# ---------------------------------------------------------------------------


def sin_tildes(texto):
    """'PINDARÉ' -> 'PINDARE' (descompone y descarta los diacriticos)."""
    descompuesto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in descompuesto if unicodedata.category(c) != "Mn")


def slug(nombre):
    """'REI VERDE Padrón Arg. 500g' -> 'rei-verde-padron-arg-500g'."""
    base = re.sub(r"[^a-z0-9]+", "-", sin_tildes(nombre).lower())
    return re.sub(r"^-|-$", "", base)


def formato_precio(n):
    """10500 -> '10.500' (separador de miles rioplatense)."""
    return f"{n:,}".replace(",", ".")


# ---------------------------------------------------------------------------
# Productos
# ---------------------------------------------------------------------------


def obtener_marca(nombre):
    """Marca conocida con la que empieza el producto, o su primera palabra."""
    for marca in MARCAS_CONOCIDAS:
        if nombre.startswith(marca + " ") or nombre == marca:
            return marca
    return nombre.split(" ")[0]


def buscar_imagen(nombre_slug):
    """Ruta relativa de la foto del producto, o None si no hay ninguna."""
    for ext in EXTENSIONES:
        if (IMG_DIR / f"{nombre_slug}{ext}").is_file():
            return f"img/{nombre_slug}{ext}"
    return None


def agrupar_por_marca(productos):
    """{marca: [producto, ...]}, conservando el orden de products.json."""
    agrupados = {}
    for producto in productos:
        agrupados.setdefault(obtener_marca(producto["nombre"]), []).append(producto)
    return agrupados


# ---------------------------------------------------------------------------
# Generacion del HTML
# ---------------------------------------------------------------------------


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


def seccion(marca, productos):
    tarjetas = "\n".join(tarjeta(p) for p in productos)
    return f"""    <section class="brand-section" id="{slug(marca)}">
        <h2 class="brand-title">{html.escape(marca)}</h2>
        <div class="product-grid">
{tarjetas}
        </div>
    </section>"""


def render(agrupados, plantilla):
    """Reemplaza el marcador de la plantilla por las secciones de marca."""
    marcas = sorted(agrupados, key=lambda m: sin_tildes(m).upper())
    contenido = "\n\n".join(seccion(m, agrupados[m]) for m in marcas)
    return plantilla.replace(MARCADOR_CONTENIDO, contenido)


# ---------------------------------------------------------------------------
# Entrada
# ---------------------------------------------------------------------------


def main():
    productos = json.loads(PRODUCTOS_JSON.read_text(encoding="utf-8"))
    agrupados = agrupar_por_marca(productos)
    plantilla = PLANTILLA_HTML.read_text(encoding="utf-8")
    SALIDA_HTML.write_text(render(agrupados, plantilla), encoding="utf-8")

    con_img = sum(1 for p in productos if buscar_imagen(slug(p["nombre"])))
    print(f"index.html generado: {len(productos)} productos, {len(agrupados)} marcas.")
    print(f"Imagenes encontradas: {con_img}/{len(productos)}")


if __name__ == "__main__":
    main()
