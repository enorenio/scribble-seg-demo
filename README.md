# Method Comparison Viewer

Side-by-side visual comparison of scribble-supervised segmentation methods across the train, test1, and test2 datasets. Includes per-image mIoU, an interactive scatter for outlier hunting, and a "hardest 5" view of universally failed images.

## Three ways to view

### 1. Locally (quick)

```bash
cd vis_web
python serve.py
# then open http://localhost:8000
```

Stop with Ctrl+C. (Pick another port if 8000 is taken: `python serve.py 9000`.)

### 2. GitHub Pages (public demo)

This site is purely static — no server, no build step, no APIs. It deploys to GitHub Pages out of the box.

**Setup:**

```bash
# from the project root
cd vis_web
git init
git add .
git commit -m "Initial demo"
# create a new GitHub repo (e.g. 'scribble-seg-demo') via the GitHub UI,
# then point this directory at it:
git remote add origin git@github.com:<YOUR_USERNAME>/<REPO_NAME>.git
git branch -M main
git push -u origin main
```

Then on github.com:
1. Go to your repo → **Settings → Pages**
2. Under "Build and deployment", set **Source** to `Deploy from a branch`
3. Set **Branch** to `main` and folder to `/ (root)`
4. Click **Save**
5. Wait ~1 minute. The site is live at `https://<YOUR_USERNAME>.github.io/<REPO_NAME>/`

The first deploy can take up to 10 minutes; subsequent pushes are usually <1 minute. Settings → Pages shows build status.

**Deploy footprint:** ~110 MB (within GitHub Pages' 1 GB soft limit). 5,684 JPEG thumbnails + one HTML file + one `data.json` + this README.

### 3. Any other static host

The same files work on Netlify, Cloudflare Pages, Vercel, S3, etc. Just point them at the `vis_web/` directory as the publish root.

## How the page works

- **Three views (top tabs)**: 🗂 Common, 🚧 Hardest 5, 📊 Stats — only one active at a time.
- **Switch dataset** — `train` (228, with GT), `test1` (226), `test2` (228).
- **Sort** — by name, or by mIoU/foreground-IoU (train only — uses V4+V7 mIoU as the sort key).
- **Search** — substring of the image stem.
- **Toggle methods** — checkboxes hide/show prediction columns; GT toggle for train.
- **Bigger** — larger thumbnails for closer inspection.
- **Click any panel** — fullscreen lightbox.

### Stats view

- **Quality curve**: each method's 228 mIoU scores sorted best-first. Higher curves = better. Right side shows tail behavior.
- **fg-vs-bg scatter**: each dot = one train image, plotted by V4+V7's per-class IoUs. **Hover** for image stem + per-method breakdown; **click** to jump to that image's grid card.
- **Head-to-head matrix**: % of images where row-method beat column-method on mIoU.

### Hardest 5 view

The 5 train images where ALL methods scored lowest (mean mIoU < 0.55). Reveals universal failure modes: low-contrast figure-ground (cat-on-couch, dark-sofa), heavy clutter (bicycle in junkyard).

## Methods shown

| Color | Method | Description |
|---|---|---|
| 🔴 red | KNN k=11 | Per-image k-NN with RGB+spatial features (project's reported baseline) |
| 🔵 blue | V1 | Global U-Net, base=48, 80 epochs (5-fold OOF) |
| 🟣 purple | V3 | Global U-Net, base=64, 150 epochs, CutMix p=0.4, seed=43 |
| 🟠 orange | V4 | Same as V3 but seed=44 |
| 🟢 green | V3+V4 | V3+V4 ensemble + learned per-image threshold |
| 🟡 gold | **V4+V7** | Final: V7 trained with pseudo-labels from V3+V4, ensembled with V4 |

## Reading the metrics

- **Card header** shows V4+V7 mIoU + per-class IoUs (the final ensemble).
- **Each panel's bottom strip** shows that method's per-image mIoU (train only — test sets have no GT).
- **Top summary bar** shows mean mIoU/bg/fg per method across all 228 train images.

## Why the page is fully static

`index.html` contains all the JS inline (no build step). `data.json` is loaded once via `fetch`. Thumbnails are pre-rendered JPEG files. No backend APIs, no databases, no auth. The only reason a local server is needed (`serve.py`) is that browsers refuse `fetch()` against `file://` URLs for security; HTTP from any source works.

## Files

```
vis_web/
├── index.html       single-page app (HTML + CSS + JS, ~18KB)
├── data.json        catalog of 682 images × 6 methods + per-image metrics (~280KB)
├── serve.py         tiny localhost HTTP server for development
├── .nojekyll        tells GitHub Pages to serve files as-is (no Jekyll processing)
├── README.md        this file
├── train/           1,824 thumbnails (228 imgs × 8 panels: image, scribble, 5 methods, GT)
├── test1/           1,808 thumbnails (226 imgs × 8 panels)
└── test2/           1,824 thumbnails (228 imgs × 8 panels)
```
