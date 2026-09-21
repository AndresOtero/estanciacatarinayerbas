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
.github/        workflows/build.yml — regenera index.html en GitHub
```

## Regla de oro

**No edites `index.html` a mano** (ni desde GitHub): GitHub lo regenera
automaticamente con cada cambio y lo que se haya editado ahi se pierde. Todo
lo que se ve en la pagina sale de `data/products.json` (datos) o
`templates/template.html` (diseño).

## Cambiar un precio o el stock

1. Abri `data/products.json` y busca el producto por nombre.
2. Cambia el numero de `precio` (sin puntos: `11000`, no `11.000`) o el
   `estado`: `stock`, `sin-stock` o `pedido`.
3. Regenera y publica (ver [Publicar los cambios](#publicar-los-cambios)).

## Agregar un producto

1. Abri `data/products.json`. Es una lista; cada producto es una linea como
   esta:

   ```json
   { "nombre": "BALDO UY 1kg", "precio": 11000, "peso": "1kg", "estado": "stock" }
   ```

2. Agrega una linea nueva con el mismo formato. Fijate que todas las lineas
   menos la ultima terminan en coma. Por ejemplo, para sumar Canarias Serena
   de medio kilo a pedido:

   ```json
   { "nombre": "CANARIAS Serena 1kg", "precio": 11500, "peso": "1kg", "estado": "stock" },
   { "nombre": "CANARIAS Serena 500g", "precio": 6500, "peso": "500g", "estado": "pedido" },
   ```

   Campos:

   | Campo | Que va | Obligatorio |
   | --- | --- | --- |
   | `nombre` | Marca y variedad, tal como se muestra. Empieza con la marca en mayusculas. | si |
   | `precio` | Numero entero, sin puntos ni `$`. | si |
   | `peso` | Texto que va debajo del precio: `1kg`, `500g`, `Accesorio`. | si |
   | `estado` | `stock`, `sin-stock` o `pedido`. Si falta se asume `stock`. | no |
   | `categoria` | Solo para cosas que no son yerba, por ejemplo `"Accesorios"`. El producto se muestra en esa seccion, al final, en vez de en su marca. | no |

3. La marca se toma de la primera palabra del nombre. Si la marca tiene mas de
   una palabra (como `REI VERDE`) y es nueva, agregala a la lista
   `MARCAS_CONOCIDAS` en `scripts/build.py`, si no cada palabra queda como
   una marca distinta.

4. Dentro de una marca los productos salen en el orden en que estan en el
   archivo. Las marcas se ordenan solas alfabeticamente.

5. Si tenes foto, seguí [Agregar una foto](#agregar-una-foto). Si no, el
   producto sale con un mate 🧉 de relleno.

6. Regenera y publica (ver [Publicar los cambios](#publicar-los-cambios)).

## Agregar una foto

1. Prepara la imagen: fondo blanco o neutro, unos 500 px de alto y menos de
   50 KB. Se muestra en un recuadro de 150 x 150 px, asi que no hace falta
   mas resolucion. Formatos: `.jpg`, `.jpeg`, `.png` o `.webp`.

2. Nombrala con el nombre del producto en minusculas, sin tildes ni `ñ`, y
   con guiones en lugar de espacios y signos:

   | `nombre` en products.json | Archivo |
   | --- | --- |
   | `BALDO UY 1kg` | `img/baldo-uy-1kg.jpg` |
   | `CANARIAS Té Verde y Jengibre 1kg` | `img/canarias-te-verde-y-jengibre-1kg.jpg` |
   | `PINDARÉ 100g` | `img/pindare-100g.jpg` |
   | `Yerbera de cuero` | `img/yerbera-de-cuero.jpg` |

   El nombre tiene que coincidir exactamente con el producto, si no la foto
   no se usa. Para ver el nombre de archivo esperado sin adivinar:

   ```bash
   python3 -c "from scripts.build import slug; print(slug('CANARIAS Serena 500g'))"
   ```

3. Copia el archivo a la carpeta `img/`.

4. Regenera y publica. `build.py` avisa cuantas fotos encontro
   (`Imagenes encontradas: 27/27`); si el numero no subio, revisa el nombre.

El logo de la esquina es `img/logo.png` y el icono de la pestaña
`img/favicon.png`; para cambiarlos, reemplaza el archivo con el mismo nombre.

## Publicar los cambios

### Desde GitHub (sin instalar nada)

1. Abri el archivo en GitHub (por ejemplo `data/products.json`), toca el
   lapiz, edita y guarda con "Commit changes".
2. Listo. GitHub regenera `index.html` solo y en uno o dos minutos el cambio
   esta en <https://estanciacatarina.com>. Podes ver el progreso en la
   pestaña "Actions" del repositorio.

Para subir una foto desde GitHub: entra a la carpeta `img/`, "Add file" →
"Upload files", y despues confirma el commit. El nombre del archivo tiene que
seguir la regla de [Agregar una foto](#agregar-una-foto).

### Desde tu computadora

1. Regenera la pagina:

   ```bash
   python3 scripts/build.py
   ```

2. Miralo antes de publicar (opcional, ver abajo).

3. Sube todo, incluido el `index.html` regenerado:

   ```bash
   git add -A && git commit -m "Actualizar productos" && git push
   ```

## Ver el sitio antes de publicarlo

```bash
python3 scripts/serve.py
```

Abri <http://localhost:8000>. La pagina se regenera en cada recarga, asi que
podes editar `data/products.json` y refrescar el navegador para ver el cambio.
`Ctrl+C` corta el servidor. Para usar otro puerto: `python3 scripts/serve.py 3000`.

## Archivos

- `data/products.json` — los datos (unico archivo que hace falta editar normalmente).
- `templates/template.html` — estructura y estilos de la pagina.
- `scripts/build.py` — genera `index.html` combinando los dos anteriores.
- `scripts/serve.py` — servidor local de previsualizacion.
- `index.html` — **generado**, no editar a mano.
