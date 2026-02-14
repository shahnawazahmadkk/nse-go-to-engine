# NSE GO-TO Engine (Free Hosting)

This repo contains:
- `indicator.py` — NSE stock scanner (3 buckets + sideways mode)
- GitHub Action that runs Mon–Fri 9:00 AM IST
- Static UI hosted via GitHub Pages (HTML/CSS/JS)

## How it works
- The workflow runs `python indicator.py`
- It generates:
  - `docs/signals.json`
  - `docs/nse_*_20.csv`
- GitHub Pages serves the `docs/` folder

## Enable GitHub Pages
1. Go to Repo Settings → Pages
2. Source: Deploy from branch
3. Branch: main
4. Folder: /docs

Your site will be available at:
`https://YOUR_USERNAME.github.io/YOUR_REPO/`

## Run locally
```bash
pip install -r requirements.txt
python indicator.py
```
