import os
import time
from datetime import datetime, timezone
import pandas as pd
from pytrends.request import TrendReq
import gspread
from gspread.exceptions import WorksheetNotFound

SHEET_ID = os.environ.get("SHEET_ID")
DAILY_PN = os.environ.get("DAILY_PN", "canada")
REALTIME_PN = os.environ.get("REALTIME_PN", "CA")
REALTIME_CAT = os.environ.get("REALTIME_CAT", "all")
REALTIME_COUNT = int(os.environ.get("REALTIME_COUNT", "20"))
TZ_OFFSET_MIN = int(os.environ.get("TZ_OFFSET_MIN", "0"))

DAILY_SHEET = os.environ.get("DAILY_SHEET", "daily_trending")
REALTIME_SHEET = os.environ.get("REALTIME_SHEET", "realtime_trending")

def get_or_create_ws(sh, title, header_cols):
    try:
        ws = sh.worksheet(title)
    except WorksheetNotFound:
        ws = sh.add_worksheet(title=title, rows=2000, cols=max(10, len(header_cols)))
        ws.append_row(header_cols)
    existing = ws.row_values(1)
    if existing != header_cols:
        ws.update("A1", [header_cols])
    return ws

def append_df(ws, df: pd.DataFrame):
    if df.empty:
        return
    values = [df.columns.tolist()] + df.astype(str).values.tolist()
    if ws.row_values(1) == df.columns.tolist():
        values = values[1:]
    ws.append_rows(values, value_input_option="RAW")

def rankify(df, key_col):
    df = df.copy()
    df["rank"] = range(1, len(df) + 1)
    cols = ["run_ts", "rank"] + [c for c in df.columns if c not in ("run_ts", "rank")]
    return df[cols]

def run():
    if not SHEET_ID:
        raise SystemExit("Missing SHEET_ID env var. Set it to your Google Sheet ID.")

    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key(SHEET_ID)
    pytrends = TrendReq(hl='en-US', tz=TZ_OFFSET_MIN)
    run_ts = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # Daily trending
    try:
        daily_df = pytrends.trending_searches(pn=DAILY_PN)
        if daily_df.shape[1] == 1:
            daily_df.columns = ["query"]
        daily_df.insert(0, "run_ts", run_ts)
        daily_df = rankify(daily_df, "query")
        ws = get_or_create_ws(sh, DAILY_SHEET, daily_df.columns.tolist())
        append_df(ws, daily_df)
    except Exception as e:
        print(f"[WARN] daily trending failed: {e}")
    time.sleep(2)

    # Realtime
    try:
        rt_df = pytrends.realtime_trending_searches(pn=REALTIME_PN, cat=REALTIME_CAT, count=REALTIME_COUNT)
        keep_cols = [c for c in ["title", "entityNames", "source", "publishedAt", "traffic", "articleUrl"] if c in rt_df.columns]
        if not keep_cols:
            keep_cols = rt_df.columns.tolist()
        rt_df = rt_df[keep_cols].copy()
        rt_df.insert(0, "run_ts", run_ts)
        rt_df = rankify(rt_df, keep_cols[0] if keep_cols else "title")
        ws = get_or_create_ws(sh, REALTIME_SHEET, rt_df.columns.tolist())
        append_df(ws, rt_df)
    except Exception as e:
        print(f"[WARN] realtime trending failed: {e}")

    print("Done.")

if __name__ == "__main__":
    run()
