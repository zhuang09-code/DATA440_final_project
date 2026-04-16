import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

from src.config import DATA_URL, HEADERS
from src.text_utils import clean_text, normalize_value, parse_email, parse_webpage

def scrape_data_science_people(url: str = DATA_URL) -> pd.DataFrame:
    """
    Scrape the W&M Data Science people page and return:
    1. a pandas DataFrame
    2. the underlying list of record dictionaries
    """

    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    main = soup.find("main")
    if main is None:
        main = soup

    tokens = [clean_text(t) for t in main.stripped_strings if clean_text(t)]
    # Faculty names on this page look like: "Last, First"
    name_pattern = re.compile(r"^[A-Z][A-Za-z'’\-]+,\s+[A-Z][A-Za-z.\-\'’ ]+$")

    records = []
    current = None
    started = False
    pending_label = None

    for token in tokens:
        # Start parsing from the first faculty record
        if token == "Alam, MD Mahfuz Ibn":
            started = True

        if not started:
            continue
        
        # Stop before footer text
        if token == "Williamsburg, Virginia":
            break
        
        # Start a new faculty record when a name is found
        if name_pattern.match(token):
            if current is not None:
                records.append(current)

            current = {
                "name": token,
                "title": None,
                "office": None,
                "email_raw": None,
                "email": None,
                "areas_of_interest": None,
                "webpage_raw": None,
                "webpage": None,
                "department": "Data Science",
            }
            pending_label = None
            continue

        if current is None:
            continue
        
        # If the previous token was a label, this token should be its value
        if pending_label is not None:
            if token == ":":
                continue

            value = normalize_value(token)

            if pending_label == "office":
                current["office"] = value
            elif pending_label == "email":
                current["email_raw"] = value
                current["email"] = parse_email(value)
            elif pending_label == "areas_of_interest":
                current["areas_of_interest"] = value
            elif pending_label == "webpage":
                current["webpage_raw"] = value
                current["webpage"] = parse_webpage(value)

            pending_label = None
            continue

        lower = token.lower().rstrip(":")

        # Recognize field labels
        if lower == "office":
            pending_label = "office"
            continue
        if lower == "email":
            pending_label = "email"
            continue
        if lower == "areas of interest":
            pending_label = "areas_of_interest"
            continue
        if lower == "webpage":
            pending_label = "webpage"
            continue
        if lower == "office hours":
            pending_label = None
            continue
        
        # The first non-label token after the faculty name is treated as title
        if current["title"] is None and token != ":":
            current["title"] = token

    # Add the last faculty record
    if current is not None:
        records.append(current)

    df = pd.DataFrame(records)
    return df, records