# CLAUDE.md

See [AGENTS.md](AGENTS.md) for the full guidance. The essentials:

- **`index.html` is generated — never edit it directly.** Edit
  `data/products.json` (data) or `templates/template.html` (markup and CSS)
  instead.
- Rebuild with `python3 scripts/build.py`, and commit the regenerated
  `index.html` alongside the source change.
- Preview locally with `python3 scripts/serve.py` (http://localhost:8000); it
  rebuilds on every page load.
- **Node is not installed.** Use `python3`; the build has no dependencies.
- The page ships **no JavaScript** by design. Keep it that way.
- `index.html` and `img/` must stay at the repo root — GitHub Pages serves from
  the root of `main`.
- Pushing to `main` deploys to GitHub Pages.
- Site content is in Spanish.
