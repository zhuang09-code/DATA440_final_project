import pandas as pd
import re

text_columns = [
    "name",
    "title",
    "office",
    "email",
    "areas_of_interest",
    "webpage",
    "department",
]

def clean_cell(x: str) -> str:
    """
    Clean a single cell by removing extra whitespace.
    """
    if pd.isna(x):
        return ""
    return " ".join(str(x).split()).strip()

def make_department_webpage(name: str) -> str:
    """
    Generate a default W&M Data Science department profile URL.

    Example:
        "Alam, MD Mahfuz Ibn"
        -> "https://cdsp.wm.edu/data-science/people/alam-md.php"
    """
    if "," in name:
        last = name.split(",")[0].strip().lower()
        first = name.split(",")[1].strip().split()[0].lower()
        slug = f"{last}-{first}"
    else:
        parts = name.strip().lower().split()
        if len(parts) >= 2:
            slug = f"{parts[-1]}-{parts[0]}"
        else:
            slug = parts[0] if parts else "unknown"

    slug = re.sub(r"[^a-z0-9\-]", "", slug)

    return f"https://cdsp.wm.edu/data-science/people/{slug}.php"

def fill_missing_webpage(row: pd.Series) -> str:
    """
    Fill missing webpage values with the generated department profile URL.
    """
    webpage = row.get("webpage", "")
    name = row.get("name", "")

    if webpage == "" or webpage.lower() in ["none", "n/a", "na"]:
        return make_department_webpage(name)

    return webpage

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and prepare scraped faculty data for recommendation.
    """
    df = df.copy()

    # Remove debug columns if they exist
    df = df.drop(columns=["email_raw", "webpage_raw"], errors="ignore")

    # Make sure all expected text columns exist
    for col in text_columns:
        if col not in df.columns:
            df[col] = ""

    # Clean text columns
    for col in text_columns:
        df[col] = df[col].apply(clean_cell)

    # Remove rows without a faculty name
    df = df[df["name"] != ""].copy()

    # Remove duplicate faculty entries
    df = df.drop_duplicates(subset=["name"]).reset_index(drop=True)

    # Fill missing webpage values with generated department webpage
    df["webpage"] = df.apply(fill_missing_webpage, axis=1)

    # Build a combined text field for recommendation
    df["profile_text"] = (
        df["title"] + " "
        + df["areas_of_interest"] + " "
        + df["department"]
    ).str.strip()

    # Lowercase version for keyword matching
    df["profile_text_clean"] = df["profile_text"].str.lower()

    return df