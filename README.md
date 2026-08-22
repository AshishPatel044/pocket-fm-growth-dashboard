# Pocket FM — Growth Updates Promos Dashboard

A fully client-side HTML dashboard for the Pocket FM growth / ads team. Shows **CPS Promos** and **Scaling Promos** performance data from Meta ad campaigns.

## Live Features

| Feature | Details |
|---|---|
| **CPS Promos view** | 574+ ad sets, 74 columns, auto-analysis verdicts (Cracked / Improve / Kill) |
| **Scaling Promos view** | Scaling ad performance, D0/D3/D7/D15 cohort breakdowns |
| **Import CPS CSV** | Upload the Master Sheet CSV → dashboard updates instantly |
| **Import Scaling CSV** | Upload the New Scaling Ads CSV → dashboard updates instantly |
| **Export CSV** | Export current filtered view to CSV |
| **Recovery Month Calculator** | Type a D7 or D15 recovery % → see projected recovery month |
| **D7M / D15M columns** | Per-row recovery month badges (M1–M9+) |
| **Install Filters** | Filter Scaling rows by D0/D3/D7/D15 install count |
| **Column chooser** | Show/hide columns by group |
| **Column-level filters** | Google-Sheets style value filters per column |
| **Freeze columns** | Excel-style multi-column freeze |
| **Formula bar** | Click any cell to see full value |

## How to Update Data

1. Open the deployed dashboard.
2. Click **⬆ Import CPS CSV** → select the latest `CPS New Sheet - Master Sheet (CPS) *.csv`.
3. Click **⬆ Import Scaling CSV** → select the latest `CPS New Sheet - New Scalling Ads *.csv`.
4. The dashboard refreshes instantly — no page reload needed.

The "Data updated" date in the header updates to today's date on every import.

## Deploy on Vercel

1. Push this repo to GitHub.
2. Go to [vercel.com](https://vercel.com) → **Add New Project** → import this repo.
3. Framework: **Other** (static site). Root directory: `/`.
4. Deploy — Vercel detects `index.html` automatically.

Every `git push` to `main` redeploys automatically.

## CSV Format Requirements

| CSV | Header rows to skip | Columns |
|---|---|---|
| CPS Master Sheet | 3 | 74 |
| New Scaling Ads | 2 | 84 |

Column order must match the original Google Sheet export exactly.

## Recovery Month Logic

Projections use a compounding multiplier chain:
D7 → D15 (×1.83) → M1 (×1.91) → M2 (×1.87) → M3 (×1.38) → M4 (×1.24) → M5 (×1.17) → M6 (×1.13) → M7 (×1.086) → M8 (×1.086) → M9 (×1.086)

Target = **149%** (≈ 150% covering Ad Spend + 50% Overheads).
