import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("NAUKRI_EMAIL")
PASSWORD = os.getenv("NAUKRI_PASSWORD")

if not EMAIL or not PASSWORD:
    raise ValueError("Credentials missing in .env")