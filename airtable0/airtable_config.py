import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = "applrq5qLHjJohD40"
TABLE_NAME = "Users"

HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json"
}