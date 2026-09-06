# CLAUDE.md

See [AGENTS.md](AGENTS.md) for the full guidance. The essentials:

- **`index.html` is generated — never edit it directly.** Edit `products.json`
  (data) or `template.html` (markup and CSS) instead.
- Rebuild with `python3 build.py`, and commit the regenerated `index.html`
  alongside the source change.
- Preview locally with `python3 serve.py` (http://localhost:8000); it rebuilds
  on every page load.
- **Node is not installed.** Use `python3`; the build has no dependencies.
- The page ships **no JavaScript** by design. Keep it that way.
- Pushing to `main` deploys to GitHub Pages.
- Site content is in Spanish.
