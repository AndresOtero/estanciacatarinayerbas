# AGENTS.md

Guidance for coding agents working in this repository.
Claude Code users: see [CLAUDE.md](CLAUDE.md) for the short version.

## What this is

A static price list for Estancia Catarina Yerbas — yerba mate products grouped
by brand. Published with GitHub Pages at <https://estanciacatarina.com> (custom domain
registered at Cloudflare; the GitHub-provided URL
<https://andresotero.github.io/estanciacatarinayerbas/> redirects there).

No framework, no bundler, no dependencies. The site is plain HTML and CSS with
**zero JavaScript** — that is deliberate, so the products are visible to search
engines and link previews. Do not reintroduce client-side rendering. The stock
filter pills are pure CSS (radio inputs plus `:has()` selectors in the
template), and the brand index is generated at build time.

## The one rule that matters

**`index.html` is generated. Never edit it by hand.** Any manual change is lost
on the next build. This includes edits made through the GitHub web editor: in
September 2026 the page was rewritten by hand there, and the design had to be
ported back into the template. If someone needs to change the page, change
`data/products.json` or `templates/template.html` and rebuild.

## Layout

```
index.html            Generated output. Committed so Pages can serve it.
CNAME                 Custom domain for GitHub Pages. Do not delete or rename.
img/                  Product photos (optional), plus logo.png and favicon.png.
data/products.json    The data. Usually the only file that needs editing.
templates/template.html   Page structure and CSS. Has the <!--CONTENIDO--> placeholder.
scripts/build.py      Renders the data into the template.
scripts/serve.py      Local preview server. Rebuilds on each request.
```

`index.html` and `img/` sit at the repo root because GitHub Pages is configured
to serve from the root of `main`. Everything else is source and can live in
folders. Moving the published files into a subdirectory (e.g. `docs/`) would
also require changing the Pages source in the repository settings — do not do
it as a side effect of another change.

Both scripts resolve paths from `Path(__file__).resolve().parent.parent`, so
they work from any working directory. Nothing needs to be on `sys.path`.

## Build

```bash
python3 scripts/build.py
```

Python 3 only — **Node is not installed in this environment.** The script uses
the standard library, so there is nothing to install.

Always run the build after touching `data/products.json` or
`templates/template.html`, and commit the regenerated `index.html` in the same
commit as the source change.

## Previewing locally

```bash
python3 scripts/serve.py          # http://localhost:8000, or `… serve.py 3000`
```

It serves the repository root and regenerates `index.html` on every page load,
so editing `data/products.json` and refreshing is enough — no need to re-run
`build.py` while it is running. Use it to check a change before pushing, since
pushing to `main` publishes immediately.

Note it still writes `index.html` to disk, so commit or discard that file
deliberately after a preview session.

## Deploying

GitHub Pages builds from the `main` branch, root directory. Pushing to `main`
publishes; there is no CI workflow and no build step on GitHub's side. Allow a
minute or so for the Pages build.

The custom domain lives in the `CNAME` file at the repo root (one line,
`estanciacatarina.com`). GitHub Pages reads it on every deploy, so deleting it
would drop the domain. `build.py` does not touch it. DNS is managed in the
Cloudflare dashboard: A records for the apex pointing at GitHub Pages' IPs and
a `www` CNAME to `andresotero.github.io`, with the Cloudflare proxy off (DNS
only) so GitHub can issue the HTTPS certificate.

## Product images

Photos are shown in a 150 px box with `object-fit: contain`, so keep them
small (about 500 px on the long side, under 50 KB). Do not embed images as
base64 in the page; put files in `img/` instead.

`build.py` looks for `img/<slug>.<ext>` where `ext` is `.jpg`, `.jpeg`, `.png`
or `.webp`. The slug is the product name lowercased, with accents stripped and
every run of non-alphanumeric characters replaced by a hyphen:

| Product | Expected file |
| --- | --- |
| `BALDO UY 1kg` | `img/baldo-uy-1kg.jpg` |
| `CANARIAS Té Verde y Jengibre 500g` | `img/canarias-te-verde-y-jengibre-500g.jpg` |
| `REI VERDE Padrón Arg. 500g` | `img/rei-verde-padron-arg-500g.jpg` |

Detection happens at build time. When no file matches, the card renders a
placeholder instead — so there is never a broken-image icon, and adding photos
is just a matter of dropping files in and rebuilding.

## Product fields

```json
{ "nombre": "BALDO UY 1kg", "precio": 11000, "peso": "1kg", "estado": "stock" }
```

- `estado`: one of `stock`, `sin-stock`, `pedido` (the keys of `ESTADOS` in
  `build.py`). Missing means `stock`; anything else fails the build with a
  message naming the product. The same keys appear in the template's filter
  selectors (`#filtro-stock` etc.), so renaming one means touching both.
- `categoria`: optional. When present it replaces the brand as the product's
  group. Groups listed in `GRUPOS_FINALES` (currently just `Accesorios`) render
  after the brands, in that order.

## Brand grouping

Brands come from the `MARCAS_CONOCIDAS` list in `scripts/build.py`. The literal
is kept alphabetical for maintenance, and sorted longest-first at import on
purpose, so `REI VERDE Premium 1kg` matches `REI VERDE` rather than a shorter
prefix. A product whose brand is not in the list falls back to its first word,
which is usually right but not always.

**When adding a product from a new multi-word brand, add that brand to the
list** — otherwise it gets split into the wrong group.

Within a brand, cards render in the order the products appear in
`data/products.json`. The brand sections themselves are sorted alphabetically,
ignoring accents.

## Conventions

- All user-facing content is in **Spanish**. Keep copy, headings and commit
  messages consistent with what is already there.
- Prices are integers in `data/products.json`; the build formats them with a `.`
  thousands separator (`10500` renders as `10.500`).
- Keep the CSS in `templates/template.html`. There is no separate stylesheet.
  The colour palette is defined once as custom properties in `:root`; reuse
  those variables instead of hardcoding new hex values.
- The template loads the Fraunces and Inter fonts from Google Fonts. That is
  the only external request the page makes.
