import pandas as pd
from src.scrape_deparment import scrape_data_science_people
from src.preprocess import preprocess_data
from src.research_scraper import get_papers
from src.scoring import compute_faculty_relevance
from src.text_utils import fix_name

def generate_data(keywords: list[str]) -> pd.DataFrame:
    """
    Generate a ranked faculty dataframe based on the user's research interests.
    This function runs the full recommendation pipeline:
    1. Scrape faculty information from the department website.
    2. Preprocess the faculty data into a clean dataframe.
    3. Retrieve research papers for each faculty member.
    4. Compute a relevance score for each faculty member based on the input research interests.
    5. Rank faculty members by their normalized relevance score.
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
        result = compute_faculty_relevance(papers, keywords)
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