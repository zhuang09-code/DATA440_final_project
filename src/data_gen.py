import pandas as pd
from src.scrape_deparment import scrape_data_science_people
from src.preprocess import preprocess_data
from src.research_scraper import get_papers
from src.scoring import compute_faculty_relevance
from src.text_utils import fix_name

def generate_data(keyword: str) -> pd.DataFrame:
    """
    Full pipeline:
    faculty → papers → scoring → ranking
    """

    # 1. Load faculty data
    df, _ = scrape_data_science_people()
    df = preprocess_data(df)

    # 2. storage
    scores = []
    keyword_counts = []
    total_papers_list = []

    # 3. iterate faculty
    for name in df["name"]:
        papers = get_papers(fix_name(name)) or []

        result = compute_faculty_relevance(papers, keyword)

        keyword_counts.append(result["keyword_count"])
        total_papers_list.append(result["total_papers"])
        scores.append(result["score"])

    # 4. attach results
    df["keyword_count"] = keyword_counts
    df["total_papers"] = total_papers_list
    df["score"] = scores

    # 5. rank by score
    df_sorted = df.sort_values(by="score", ascending=False).reset_index(drop=True)

    return df_sorted