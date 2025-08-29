# Agency Automations (Monorepo)

Free, scalable automations for your first 15–20 clients. Start with **Pytrends → Google Sheets** using GitHub Actions.

## What’s inside
- `pytrends-to-sheets/` — reusable automation template
- `.github/workflows/pytrends-matrix.yml` — daily schedule; run for many clients via **environments input**
- `clients.csv` — optional tracker of clients (slug, sheet id)
- `.github/workflows/weekly-report.yml` — weekly report generator (free artifact + Sheet tab)
- `tools/onboard_client.md` — add a client in 60 seconds

## Quick start
1) Create this repo in your org and push these files.
2) For a single test client, use `pytrends-to-sheets/.github/workflows/run.yml` and set repo secrets:
   - `SHEET_ID`
   - `GCP_SERVICE_ACCOUNT_JSON`
3) To run for **many clients**, create a GitHub **Environment** per client (e.g. `client-acme`) and add environment secrets:
   - `SHEET_ID`
   - `GCP_SERVICE_ACCOUNT_JSON`
   Then run **Pytrends (Matrix)** with input: `client-acme,client-zen`.

## Optional: clients.csv
You can also list your clients in `clients.csv` to keep track of slugs and Sheet IDs. The weekly report job will read it when you trigger it manually.

## Cost
- GitHub Actions (public repo) — free
- Google Sheets API — free
- Pytrends — free (unofficial)

## Notes
- Use a **separate** Google service account per client.
- Share each client’s Google Sheet with that service account (Editor).
- Keep all creds in GitHub **secrets**/**environment secrets**.
