import pandas as pd
from src.scrape_deparment import scrape_data_science_people
from src.preprocess import preprocess_data
from src.research_scraper import get_papers
from src.scoring import  profile_base_score, compute_faculty_relevance
from src.text_utils import fix_name

def generate_data(keywords: str | list[str]) -> pd.DataFrame:
    """
    Generate a ranked faculty dataframe based on the user's research interests.

    This function runs the full recommendation pipeline:
    1. Scrape faculty information from the department website.
    2. Preprocess the faculty data into a clean dataframe.
    3. Compute a base relevance score using department profile information.
    4. Retrieve publication data from Semantic Scholar when available.
    5. Compute a publication-based relevance score.
    6. Combine the profile score and publication score.
    7. Rank faculty members by the final combined relevance score.
    """
    
    if isinstance(keywords, str):
        keywords = [keywords]

    keywords = [k.strip() for k in keywords if k.strip()]

    if not keywords:
        raise ValueError("At least one research interest keyword is required.")

    df, _ = scrape_data_science_people()
    df = preprocess_data(df)

    profile_scores = []
    profile_keyword_counts = []
    publication_scores = []
    publication_keyword_counts = []
    total_papers_list = []
    final_scores = []
    score_sources = []

    for _, row in df.iterrows():
        name = row["name"]

        profile_result = profile_base_score(row, keywords)

        papers = get_papers(fix_name(name)) or []

        if papers:
            paper_result = compute_faculty_relevance(papers, keywords)
            publication_score = paper_result["score"]
            publication_keyword_count = paper_result["keyword_count"]
            total_papers = paper_result["total_papers"]
            score_source = "profile_and_semantic_scholar"
        else:
            publication_score = 0
            publication_keyword_count = 0
            total_papers = 0
            score_source = "faculty_profile_only"

        final_score = profile_result["profile_score"] + 0.5 * publication_score

        profile_scores.append(profile_result["profile_score"])
        profile_keyword_counts.append(profile_result["profile_keyword_count"])
        publication_scores.append(publication_score)
        publication_keyword_counts.append(publication_keyword_count)
        total_papers_list.append(total_papers)
        final_scores.append(final_score)
        score_sources.append(score_source)

    df["profile_keyword_count"] = profile_keyword_counts
    df["profile_score"] = profile_scores
    df["publication_keyword_count"] = publication_keyword_counts
    df["total_papers"] = total_papers_list
    df["publication_score"] = publication_scores
    df["score"] = final_scores
    df["score_source"] = score_sources

    df_sorted = df.sort_values(
        by=["score", "profile_score", "publication_score"],
        ascending=[False, False, False]
    ).reset_index(drop=True)

    return df_sorted