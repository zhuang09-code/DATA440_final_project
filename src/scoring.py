from numpy.char import title
import pandas as pd

def profile_base_score(row: pd.Series, keywords: list[str]) -> dict:
    """
    Compute a base relevance score using faculty profile information.

    The profile score is based on whether the user's research interest keywords
    appear in the faculty member's title, areas of interest, or department field.
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
        "profile_keyword_count": keyword_count,
        "profile_score": score
    }

def compute_keyword_count(papers: list, keywords: list[str]) -> int:
    """
    Count how many papers contain at least one keyword.
    """
    lowered_keywords = [k.lower().strip() for k in keywords if k.strip()]
    count = 0

    # Combine title and abstract for keyword search
    for i in papers:
        title = i.get("title") or ""
        abstract = i.get("abstract") or ""
        text = (title + " " + abstract).lower()
        
        if any(keyword in text for keyword in lowered_keywords):
            count += 1

    return count

def compute_normalized_relevance(keyword_count: int, total_papers: int, eps: float = 1e-8) -> float:
    """
    Normalize keyword count by total publications to reduce bias toward prolific authors.
    """
    return keyword_count / (total_papers + eps)

def compute_faculty_relevance(papers: list, keywords: list[str]) -> dict:
    """
    Compute overall relevance score for a faculty member.
    """
    total_papers = len(papers)
    keyword_count = compute_keyword_count(papers, keywords)
    score = compute_normalized_relevance(keyword_count, total_papers)

    return {
        "keyword_count": keyword_count,
        "total_papers": total_papers,
        "score": score
    }
