# FHLB-Topeka In-Person Day — Workshop Package

A tailored, hands-on Databricks workshop + demo kit for the **FHLB-Topeka in-person day
(Sep 17, 2026)**, built with the `workshop-builder` method and grounded in **real FHFA public
data + a synthetic FHLB core-banking book**. Everything here is **illustrative — not
FHLB-Topeka production data.**

- **Session 3 is a hands-on lab** (5 notebooks): explore governed Unity Catalog gold →
  SQL story beats → **create your own Genie space** → build a dashboard.
- **Sessions 1, 4, 5 are presenter-led demo scripts.** Sessions 2A/2B are discussion.
- **Two delivery modes**, both included: live in our workspace (**Mode A**) or a portable,
  self-contained zip that runs anywhere including Free Edition (**Mode B**).

See **`AGENDA.md`** for the full agenda-to-asset map.

## Layout
```
fhlb-topeka-workshop/
├── AGENDA.md                     # the day mapped to assets + the validated story
├── notebooks/
│   ├── 00_WORKSHOP_GUIDE.ipynb   # Session 3 hands-on lab (import these into Databricks)
│   ├── 01_explore_uc.ipynb
│   ├── 02_sql_analysis.ipynb
│   ├── 03_genie_space.ipynb      # the core exercise: your own Genie space
│   ├── 04_dashboard.ipynb
│   └── 00_LOAD_DATA.py           # Mode B portable loader (admin runs once)
├── demo-scripts/                 # presenter run-of-show for Sessions 1, 4, 5
├── instructor/                   # SETUP, RUNBOOK, DRY_RUN, ANSWER_KEY, DATA_DICTIONARY,
│                                 #   TROUBLESHOOTING, ATTENDEE_REQUIREMENTS
├── data/                         # Mode B: 6 gzipped CSVs (the analyst gold/silver tables)
└── resources/                    # nb.py, zip_workshop.py, build_notebooks.py, export_data.py
```

## Run it — Mode A (live, our workspace)
The data, Genie spaces, and apps already exist in `fevm-serverless-stable-6fhczt`
(catalog `serverless_stable_6fhczt_catalog`, schemas `fhlb_gold` / `fhlb_silver`).
1. Import `notebooks/00–04` into the workspace.
2. Confirm a **serverless SQL warehouse** is running and attendees have the grants in
   `instructor/ATTENDEE_REQUIREMENTS.md`.
3. Attendees start at `00_WORKSHOP_GUIDE`. The `CONFIG` cell already points at the live catalog.

## Run it — Mode B (portable / Free Edition)
1. On the target workspace, an admin runs `notebooks/00_LOAD_DATA.py`:
   set `CATALOG` (default `fhlb_workshop`), Run All, and upload the 6 files from `data/`
   into the volume it creates when prompted.
2. Set the **same `CATALOG`** value in each notebook's `CONFIG` cell.
3. Verify the headline: the loader's last cell should show **Midwest Savings Bank ≈ 24.3%**.

> **Note:** creating a *new* catalog needs workspace/metastore admin. **No `CREATE CATALOG`?** Set the
> `catalog` widget in `00_LOAD_DATA` to an **existing** catalog you can write to (`CREATE SCHEMA` on it)
> — the loader reuses it and skips creation. Our `fevm` identity is denied catalog creation, so Mode B
> runs on a *target* (Free Edition / demo) workspace or an existing catalog — see `instructor/DRY_RUN.md`.

## Rebuild the assets
```bash
cd resources
python3 build_notebooks.py     # regenerate the 5 Session 3 notebooks
python3 export_data.py         # re-export the 6 gzipped CSVs from fevm (needs the fevm profile)
python3 zip_workshop.py .. ../fhlb-topeka-workshop.zip   # package with directory entries
```

## The data
~92% is **real public regulatory data** (FHFA House Price Index, FHFA FHLBank member
acquisitions/PUDB, Federal Reserve DFAST stress paths); ~8% is a **synthetic core-banking
book** (members, advances, collateral, MPF loans). Details and every validated number:
`instructor/DATA_DICTIONARY.md`.

*Built by Field Engineering with the workshop-builder skill, from the FHLB-Topeka demo build.*
