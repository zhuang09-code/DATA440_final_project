import pandas as pd

def display_top_professors(df: pd.DataFrame, top_n: int = 3) -> None:
    """
    Display the top N professors based on score.
    Inputs:
        df: DataFrame containing faculty information and scores.
        top_n: Number of top professors to display. (3 is set as default)
    Output: 
        Prints the top professors with their title and matching paper count.
    
    Displayed Format Example:
        1. Ford, Trenton
        Title: Assistant Professor of Data Science
        Office: Integrated Science Center 3321
        Email: twford@wm.edu
        Matching Papers: 15
        --------------------------------------------------
    """

    # Sort by score (descending), then keyword_count as tiebreaker
    top_df = df.sort_values(
        by=["score", "keyword_count"],
        ascending=False
    ).head(top_n)

    # Output the top professors in a readable format
    print("\nTop Professors Based on Your Research Interest:\n")

    for i, row in enumerate(top_df.itertuples(), start=1):
        print(f"{i}. {row.name}")
        print(f"   Title: {row.title}")
        print(f"   Office: {row.office}")
        print(f"   Email: {row.email}")
        print(f"   Webpage: {row.webpage}")
        print(f"   Matching Papers: {row.keyword_count}")
        print("-" * 50)
    
    return None