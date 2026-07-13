# Muxy Documentation Site

This repository contains the GitHub Pages version of the exported Muxy ReadMe documentation.

## Local Preview

```powershell
python -m pip install -r requirements.txt
python scripts/migrate_readme_export.py
mkdocs serve
```

## Build

```powershell
mkdocs build --strict
```

## Publish

The GitHub Actions workflow in `.github/workflows/deploy.yml` publishes the built site to GitHub Pages.

