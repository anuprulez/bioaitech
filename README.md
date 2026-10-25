# BioAI Tech

The source code for [bioaitech.org](https://bioaitech.org), a lightweight static website focused on artificial intelligence in life science.

The site is built with Python, Markdown, HTML, CSS, and vanilla JavaScript. It has no third-party runtime dependencies and is deployed automatically through GitHub Pages.

## Features

- Markdown-based page content
- Shared HTML templates
- Responsive, accessible design
- Automated sitemap and `robots.txt` generation
- Automated deployment with GitHub Actions
- No JavaScript framework or package manager required

## Project structure

```text
.
├── content/               # Page content written in Markdown
├── static/                # Styles, scripts, icons, and social assets
├── templates/             # Shared HTML templates
├── scripts/build.sh       # Build entry point
├── build.py               # Static-site generator
├── CNAME                  # GitHub Pages custom-domain declaration
└── .github/workflows/     # Deployment workflow
```

Generated files are written to `dist/`. This directory is excluded from version control.

## Requirements

- Python 3.10 or newer
- A POSIX-compatible shell

No additional Python packages are required.

## Local development

Build the site:

```bash
./scripts/build.sh
```

Start a local development server:

```bash
python3 -m http.server 8000 --directory dist
```

Open [http://localhost:8000](http://localhost:8000) in a browser.

After changing content, templates, or static assets, run the build command again and refresh the page.

## Editing content

Page content lives in `content/`:

- `content/index.md` — home page
- `content/privacy.md` — privacy page

The shared document layout and metadata are defined in `templates/base.html`. Visual styling and browser behavior live in `static/style.css` and `static/main.js`.

## Deployment

Push changes to the `main` branch. The GitHub Actions workflow builds the project and deploys the generated `dist/` directory to GitHub Pages.

Deployment progress is available in the repository's **Actions** tab.

## Build output

The build process creates:

- Rendered HTML pages
- Static assets
- `robots.txt`
- `sitemap.xml`
- GitHub Pages metadata

To verify a production build locally, run `./scripts/build.sh` and serve the result using the command above.
