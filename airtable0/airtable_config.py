import os

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY") or "patytBrY3zzezBUHw.f757442f5d299d359b1439b51ab590ef590b248be5bd910dc7b92b4374749a63"
BASE_ID = "applrq5qLHjJohD40"
TABLE_NAME = "Users"

HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json"
}
