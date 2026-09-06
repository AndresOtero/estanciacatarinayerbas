# AGENTS.md

Guidance for coding agents working in this repository.
Claude Code users: see [CLAUDE.md](CLAUDE.md) for the short version.

## What this is

A static price list for Estancia Catarina Yerbas — yerba mate products grouped
by brand. Published with GitHub Pages at
<https://andresotero.github.io/estanciacatarinayerbas/>.

No framework, no bundler, no dependencies. The site is plain HTML and CSS with
**zero JavaScript** — that is deliberate, so the products are visible to search
engines and link previews. Do not reintroduce client-side rendering.

## The one rule that matters

**`index.html` is generated. Never edit it by hand.** Any manual change is lost
on the next build.

| File | Role |
| --- | --- |
| `products.json` | The data. Usually the only file that needs editing. |
| `template.html` | Page structure and CSS. Contains the `<!--CONTENIDO-->` placeholder. |
| `build.py` | Renders `products.json` into `template.html`. |
| `index.html` | **Generated output.** Committed so Pages can serve it. |
| `img/` | Product photos, optional. |

## Build

```bash
python3 build.py
```

Python 3 only — **Node is not installed in this environment.** The script uses
the standard library, so there is nothing to install.

Always run the build after touching `products.json` or `template.html`, and
commit the regenerated `index.html` in the same commit as the source change.

## Deploying

GitHub Pages builds from the `main` branch, root directory. Pushing to `main`
publishes; there is no CI workflow and no build step on GitHub's side. Allow a
minute or so for the Pages build.

If a custom domain is configured later, GitHub adds a `CNAME` file at the repo
root. `build.py` does not touch it — leave it in place.

## Product images

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

## Brand grouping

Brands come from the `MARCAS_CONOCIDAS` list in `build.py`. It is sorted
longest-first on purpose, so `REI VERDE Premium 1kg` matches `REI VERDE` rather
than a shorter prefix. A product whose brand is not in the list falls back to
its first word, which is usually right but not always.

**When adding a product from a new multi-word brand, add that brand to the
list** — otherwise it gets split into the wrong group.

## Conventions

- All user-facing content is in **Spanish**. Keep copy, headings and commit
  messages consistent with what is already there.
- Prices are integers in `products.json`; the build formats them with a `.`
  thousands separator (`10500` renders as `10.500`).
- Keep the CSS in `template.html`. There is no separate stylesheet.
