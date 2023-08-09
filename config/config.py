import os

from dotenv import load_dotenv, find_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv(find_dotenv())

URL = os.environ.get("URL")
TECH_USER = os.environ.get("TECH_USER")
TECH_TOKEN = os.environ.get("TECH_TOKEN")
AUTH = HTTPBasicAuth(username=TECH_USER, password=TECH_TOKEN)
WRONG_CREDS = [
    HTTPBasicAuth(username=TECH_USER, password="wrong"),
    HTTPBasicAuth(username="wrong", password=TECH_TOKEN),
    HTTPBasicAuth(username=None, password=None),
    HTTPBasicAuth(username="", password="")
]
