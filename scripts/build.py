#!/usr/bin/env python3
"""Genera index.html (estatico, sin JavaScript) a partir de products.json.

Uso:  python3 scripts/build.py   (desde la raiz del repositorio)

Lee data/products.json, lo inserta en templates/template.html y escribe
index.html en la raiz, que es de donde lo publica GitHub Pages.

Las imagenes se buscan en img/<slug>.<jpg|jpeg|png|webp>. Si no existe
ninguna, la tarjeta se genera directamente con el placeholder.

Cada producto puede indicar "estado" (stock | sin-stock | pedido; por defecto
stock) y "categoria" (por ejemplo "Accesorios"), que reemplaza a la marca
como grupo y se muestra al final.
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

# Estado de stock -> (texto de la etiqueta, clase CSS extra). El estado por
# defecto es "stock". Los filtros de la plantilla usan estas mismas claves en
# el atributo data-estado, asi que no hay que renombrarlas a la ligera.
ESTADOS = {
    "stock": ("✅ En stock", ""),
    "sin-stock": ("❌ Sin stock", "sin-stock"),
    "pedido": ("🕒 A pedido", "pedido"),
}
ESTADO_POR_DEFECTO = "stock"

# Grupos que van al final, despues de las marcas, en este orden.
GRUPOS_FINALES = ["Accesorios"]

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


def obtener_estado(producto):
    """Clave de ESTADOS del producto; falla con un mensaje claro si es invalida."""
    estado = producto.get("estado", ESTADO_POR_DEFECTO)
    if estado not in ESTADOS:
        validos = ", ".join(ESTADOS)
        raise ValueError(
            f'"{producto["nombre"]}": estado "{estado}" no valido (usar {validos})'
        )
    return estado


def obtener_grupo(producto):
    """La categoria explicita si la hay; si no, la marca."""
    return producto.get("categoria") or obtener_marca(producto["nombre"])


def agrupar(productos):
    """{grupo: [producto, ...]}, conservando el orden de products.json."""
    agrupados = {}
    for producto in productos:
        agrupados.setdefault(obtener_grupo(producto), []).append(producto)
    return agrupados


def ordenar_grupos(agrupados):
    """Marcas alfabeticamente (sin tildes) y GRUPOS_FINALES al final."""
    marcas = sorted(
        (g for g in agrupados if g not in GRUPOS_FINALES),
        key=lambda g: sin_tildes(g).upper(),
    )
    return marcas + [g for g in GRUPOS_FINALES if g in agrupados]


# ---------------------------------------------------------------------------
# Generacion del HTML
# ---------------------------------------------------------------------------


def tarjeta(producto):
    nombre = producto["nombre"]
    nombre_esc = html.escape(nombre)
    ruta = buscar_imagen(slug(nombre))
    estado = obtener_estado(producto)
    texto_estado, clase_estado = ESTADOS[estado]
    clase_extra = f" {clase_estado}" if clase_estado else ""

    if ruta:
        medio = (
            f'<img src="{html.escape(ruta)}" alt="Foto de {nombre_esc}" '
            f'width="150" height="150" loading="lazy" decoding="async" />'
        )
    else:
        medio = '<div class="no-photo" aria-hidden="true">🧉</div>'

    return f"""            <article class="product-card{clase_extra}" data-estado="{estado}">
                <span class="stock-badge{clase_extra}">{texto_estado}</span>
                <div class="product-image-wrap">{medio}</div>
                <div class="product-info">
                    <h3 class="product-name">{nombre_esc}</h3>
                    <p class="product-price">{formato_precio(producto["precio"])}</p>
                    <p class="product-weight">{html.escape(producto["peso"])}</p>
                </div>
            </article>"""


def plural(n, singular="producto"):
    return f"{n} {singular}" if n == 1 else f"{n} {singular}s"


def seccion(grupo, productos):
    tarjetas = "\n".join(tarjeta(p) for p in productos)
    return f"""    <section class="brand-section" id="{slug(grupo)}">
        <div class="brand-header">
            <h2 class="brand-title">{html.escape(grupo)}</h2>
            <span class="brand-count">{plural(len(productos))}</span>
        </div>
        <div class="product-grid">
{tarjetas}
        </div>
    </section>"""


def enlace_nav(grupo, productos):
    """Enlace del indice. data-estados permite ocultarlo cuando se filtra."""
    estados = " ".join(sorted({obtener_estado(p) for p in productos}))
    return (
        f'    <a href="#{slug(grupo)}" data-estados="{estados}">'
        f"{html.escape(grupo)}</a>"
    )


def render(agrupados, plantilla):
    """Reemplaza el marcador de la plantilla por el indice y las secciones."""
    grupos = ordenar_grupos(agrupados)
    nav = "\n".join(enlace_nav(g, agrupados[g]) for g in grupos)
    secciones = "\n\n".join(seccion(g, agrupados[g]) for g in grupos)
    contenido = f"""<nav class="brand-nav" aria-label="Marcas">
{nav}
</nav>

<main class="contenido">
{secciones}
</main>"""
    return plantilla.replace(MARCADOR_CONTENIDO, contenido)


# ---------------------------------------------------------------------------
# Entrada
# ---------------------------------------------------------------------------


def main():
    productos = json.loads(PRODUCTOS_JSON.read_text(encoding="utf-8"))
    agrupados = agrupar(productos)
    plantilla = PLANTILLA_HTML.read_text(encoding="utf-8")
    SALIDA_HTML.write_text(render(agrupados, plantilla), encoding="utf-8")

    con_img = sum(1 for p in productos if buscar_imagen(slug(p["nombre"])))
    print(f"index.html generado: {len(productos)} productos, {len(agrupados)} grupos.")
    print(f"Imagenes encontradas: {con_img}/{len(productos)}")


if __name__ == "__main__":
    main()
