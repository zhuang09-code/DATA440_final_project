import json
import pandas as pd
from pathlib import Path

def save_df(df: pd.DataFrame, csv_path: str, json_path: str = None) -> None:
    """
    Save a DataFrame to a csv file and optionally to a json file.
    The function also creates parent directories if needed. 

    Parameters
    df: pandas.DataFrame
        The DataFrame to save.
    csv_path: str
        The file path where the csv output will be saved.
    json_path: str or None, optional
        The file path where the json output will be saved. If None,
        no json file will be created.
    """

    csv_file = Path(csv_path)
    csv_file.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(csv_file, index=False)

    if json_path is not None:
        json_file = Path(json_path)
        json_file.parent.mkdir(parents=True, exist_ok=True)

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(df.to_dict(orient="records"), f, indent=2, ensure_ascii=False)
    
    return None