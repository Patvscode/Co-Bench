# 🎈 Co‑Bench: Generative Co‑Workspace

A **multitool, generative workspace** built on Streamlit. It starts as a minimal template but is intended to evolve into a collaborative UI/UX where you (the user) and the assistant can:

- Add, configure, and run custom tools/modules directly from the web UI.
- Save and restore workspace state (JSON) so you can continue later.
- Sync changes automatically to a GitHub repository for backup and remote access.
- Access the app from any device, including your iPhone via Tailscale.

The repository currently contains a simple Streamlit app; the next steps will flesh out the module system and remote accessibility.

### How to run it locally

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```

Feel free to extend the workspace as needed!

## Accessing the web tools

You can open these pages from any device (including your iPhone) using the public GitHub Pages URL for this repository. After the repository is pushed to GitHub, enable **Settings → Pages → Source: main / (root)**. GitHub will publish the `web/` folder at:

- **Simple Clicker Game**: `https://<YOUR_GITHUB_USERNAME>.github.io/Co-Bench/web/game.html`
- **Random Quote Generator**: `https://<YOUR_GITHUB_USERNAME>.github.io/Co-Bench/web/tool.html`

These links work over the internet, no local network needed. Just replace `<YOUR_GITHUB_USERNAME>` with the account that owns the repo.

If you prefer a quick test without enabling Pages, you can also use the raw URLs (they render correctly in most mobile browsers):

- `https://raw.githubusercontent.com/<YOUR_GITHUB_USERNAME>/Co-Bench/main/web/game.html`
- `https://raw.githubusercontent.com/<YOUR_GITHUB_USERNAME>/Co-Bench/main/web/tool.html`

---

A simple Streamlit app template for you to modify!

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
