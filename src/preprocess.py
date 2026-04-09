import pandas as pd

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

    # Build a combined text field for recommendation
    df["profile_text"] = (
        df["title"] + " "
        + df["areas_of_interest"] + " "
        + df["department"]
    ).str.strip()

    # Lowercase version for keyword matching
    df["profile_text_clean"] = df["profile_text"].str.lower()

    return df