# BioAI Tech

Python + Markdown source for [bioaitech.org](https://bioaitech.org).

## Develop

Edit `content/*.md`, then run:

```bash
./scripts/build.sh
python3 -m http.server 8000 --directory dist
```

No third-party Python packages are required.

## Deploy to the domain

Push `main`; the GitHub Actions workflow builds and deploys to GitHub Pages. In repository **Settings → Pages**, choose **GitHub Actions** as the source. At your DNS provider, add four A records for host `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, and `185.199.111.153`. Add a CNAME record for `www` pointing to `anuprulez.github.io`. Remove conflicting records, wait for DNS propagation, then enable **Enforce HTTPS** in Pages.

The tracked `CNAME` preserves the custom domain. Content is in `content/`, layout in `templates/`, assets in `static/`, and the generated (ignored) site in `dist/`.
