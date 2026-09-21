# Estancia Catarina Yerbas — lista de precios

Sitio estatico (sin JavaScript) publicado con GitHub Pages en
<https://estanciacatarina.com>.

## Estructura

```
index.html      generado — lo publica GitHub Pages, no editar a mano
CNAME           dominio personalizado (estanciacatarina.com), no borrar
img/            fotos de los productos
data/           products.json — los datos
templates/      template.html — estructura y estilos
scripts/        build.py y serve.py
```

## Actualizar precios, stock o productos

1. Edita `data/products.json`. Cada producto tiene esta forma:

   ```json
   { "nombre": "BALDO UY 1kg", "precio": 11000, "peso": "1kg", "estado": "stock" }
   ```

   - `estado`: `stock` (en stock), `sin-stock` o `pedido` (a pedido). Si falta,
     se asume `stock`.
   - `categoria`: opcional. Por ejemplo `"Accesorios"` agrupa el producto en esa
     seccion (al final de la pagina) en vez de en su marca.

2. Regenera la pagina:

   ```bash
   python3 scripts/build.py
   ```

3. Sube los cambios:

   ```bash
   git add -A && git commit -m "Actualizar precios" && git push
   ```

## Ver el sitio antes de publicarlo

```bash
python3 scripts/serve.py
```

Abri <http://localhost:8000>. La pagina se regenera en cada recarga, asi que
podes editar `data/products.json` y refrescar el navegador para ver el cambio.
`Ctrl+C` corta el servidor. Para usar otro puerto: `python3 scripts/serve.py 3000`.

## Agregar fotos

Coloca las imagenes en `img/` con el nombre del producto en minusculas, sin
tildes y con guiones. Formatos aceptados: `.jpg`, `.jpeg`, `.png`, `.webp`.
Conviene que sean chicas (unos 500 px de alto, menos de 50 KB): se muestran en
un recuadro de 150 px. El logo es `img/logo.png` y el icono de la pestaña
`img/favicon.png`.

| Producto | Archivo |
| --- | --- |
| BALDO UY 1kg | `img/baldo-uy-1kg.jpg` |
| CANARIAS Té Verde y Jengibre 500g | `img/canarias-te-verde-y-jengibre-500g.jpg` |
| REI VERDE Padrón Arg. 500g | `img/rei-verde-padron-arg-500g.jpg` |

Despues de copiarlas, ejecuta `python3 scripts/build.py` otra vez: el script
detecta las imagenes existentes y reemplaza el placeholder por la foto.

**No edites `index.html` a mano** (ni desde GitHub): se regenera con cada
build y los cambios se pierden. Todo lo que se ve en la pagina sale de
`data/products.json` (datos) o `templates/template.html` (diseño).

## Archivos

- `data/products.json` — los datos (unico archivo que hace falta editar normalmente).
- `templates/template.html` — estructura y estilos de la pagina.
- `scripts/build.py` — genera `index.html` combinando los dos anteriores.
- `scripts/serve.py` — servidor local de previsualizacion.
- `index.html` — **generado**, no editar a mano.
