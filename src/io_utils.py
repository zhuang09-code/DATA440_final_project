import json
from pathlib import Path

def save_data(df, csv_path="data/raw/faculty_people_page.csv",
              json_path="data/raw/faculty_people_page.json"):
    """
    Save cleaned output files.

    Note:
    - email_raw and webpage_raw are kept internally for debugging,
      but excluded from final saved output files.
    """
    
    csv_file = Path(csv_path)
    json_file = Path(json_path)

    csv_file.parent.mkdir(parents=True, exist_ok=True)
    json_file.parent.mkdir(parents=True, exist_ok=True)

    output_df = df.drop(columns=["email_raw", "webpage_raw"], errors="ignore")
    output_df.to_csv(csv_file, index=False)

    output_records = output_df.to_dict(orient="records")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(output_records, f, indent=2, ensure_ascii=False)