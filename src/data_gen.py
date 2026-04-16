import pandas as pd
from src.scrape_ds import scrape_data_science_people
from src.preprocess import preprocess_data
from src.research_scraper import get_papers, count_keyword

keyword = "example_keyword"

def fix_name(name: str) -> str:
    """
    Fix the name format from "Last, First" to "First Last" for better search results in Semantic Scholar.
        Args:
            name (str): The name in "Last, First" format.
    """
    if "," in name:
        last, first = name.split(",", 1)
        return first.strip() + " " + last.strip()
    return name

def generate_data(keyword: str) -> pd.DataFrame:
    """
    Generate the final dataframe with research counts and total papers for each faculty member.
    This function combines the data scraping, preprocessing, and research paper analysis steps.

    Args:
        keyword (str): The keyword to search for in the research papers.
    """

    # Getting the faculty data and preprocessing it to get the final dataframe
    df, _ = scrape_data_science_people()
    df = preprocess_data(df)

    # Getting the research counts and total papers to get the final dataframe 
    research_counts = []
    total_papers_list = []  

    for name in df["name"]:
        papers = get_papers(fix_name(name))
    
        total_papers = len(papers)
        keyword_count = count_keyword(papers, keyword=keyword)

        research_counts.append(keyword_count)
        total_papers_list.append(total_papers)  

    df["total_papers"] = total_papers_list
    df["keyword_count"] = research_counts
    
    # Rank Professors based on keyword count and total papers
    df_sorted = df.sort_values(by=["keyword_count"], ascending=False).reset_index(drop=True)
    
    return pd.DataFrame(df_sorted)