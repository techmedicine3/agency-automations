# Onboard a New Client

## 1) Create Google service account
- Enable **Google Sheets API**
- Create a **Service Account** + **JSON key**
- Share the client’s Google Sheet with the service account’s email as **Editor**

## 2) Add a GitHub Environment (recommended)
- Repo → Settings → Environments → New environment
  - Name: `client-<slug>` (e.g., `client-acme`)
  - Add **environment secrets**:
    - `SHEET_ID` — Google Sheet ID
    - `GCP_SERVICE_ACCOUNT_JSON` — full JSON from the key file

## 3) Run daily job for multiple clients
- Actions → **Pytrends (Matrix)** → Run workflow
- Input: comma-separated list of environment names (e.g., `client-acme,client-zen`)

## 4) (Optional) Track in clients.csv
- Add a row: `client-acme,<sheet_id>`
- The weekly report job can use this list.
