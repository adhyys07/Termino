import os
from dotenv import load_dotenv
load_dotenv()
import os

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = "applrq5qLHjJohD40"
TABLE_NAME = "Users"

HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json"
}
