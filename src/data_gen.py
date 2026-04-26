import pandas as pd
from src.scrape_deparment import scrape_data_science_people
from src.preprocess import preprocess_data
from src.research_scraper import get_papers
from src.scoring import compute_faculty_relevance
from src.text_utils import fix_name

def profile_fallback_score(row: pd.Series, keywords: list[str]) -> dict:
    """
    Compute a fallback relevance score using faculty profile information
    when no Semantic Scholar papers are found.
    """
    text = (
        str(row.get("title", "")) + " "
        + str(row.get("areas_of_interest", "")) + " "
        + str(row.get("department", ""))
    ).lower()

    lowered_keywords = [k.lower().strip() for k in keywords if k.strip()]
    keyword_count = sum(1 for keyword in lowered_keywords if keyword in text)

    score = keyword_count / max(len(lowered_keywords), 1)

    return {
        "keyword_count": keyword_count,
        "total_papers": 0,
        "score": score,
        "score_source": "faculty_profile"
    }

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
    
    if isinstance(keywords, str):
        keywords = [keywords]

    keywords = [k.strip() for k in keywords if k.strip()]

    if not keywords:
        raise ValueError("At least one research interest keyword is required.")

    # 1. Load faculty data
    df, _ = scrape_data_science_people()
    df = preprocess_data(df)

    # 2. storage
    scores = []
    keyword_counts = []
    total_papers_list = []
    score_sources = []

    # 3. iterate faculty
    for _, row in df.iterrows():
        name = row["name"]
        papers = get_papers(fix_name(name)) or []

        if papers:
            result = compute_faculty_relevance(papers, keywords)
            result["score_source"] = "semantic_scholar"
        else:
            result = profile_fallback_score(row, keywords)

        keyword_counts.append(result["keyword_count"])
        total_papers_list.append(result["total_papers"])
        scores.append(result["score"])
        score_sources.append(result["score_source"])

    # 4. attach results
    df["keyword_count"] = keyword_counts
    df["total_papers"] = total_papers_list
    df["score"] = scores
    df["score_source"] = score_sources

    # 5. rank by score
    df_sorted = df.sort_values(
        by=["score", "keyword_count"],
        ascending=[False, False]
    ).reset_index(drop=True)

    return df_sorted