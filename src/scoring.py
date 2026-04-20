import numpy as np
from numpy.char import title

def compute_keyword_count(papers: list, keyword: str) -> int:
    """
    Count how many papers contain the keyword.
    """
    keyword = keyword.lower()
    count = 0

    # Combine title and abstract for keyword search
    for i in papers:
        # Handeling  for missing title or abstract
        title = i.get("title") or ""
        abstract = i.get("abstract") or ""
        
        text = (title + " " + abstract).lower()
        if keyword in text:
            count += 1

    return count


def compute_normalized_relevance(keyword_count: int, total_papers: int, eps: float = 1e-8) -> float:
    """
    Normalize keyword count by total publications to reduce bias toward prolific authors.
    """
    return keyword_count / (total_papers + eps)


def compute_faculty_relevance(papers: list, keyword: str) -> dict:
    """
    Compute overall relevance score for a faculty member.
    """
    total_papers = len(papers)
    keyword_count = compute_keyword_count(papers, keyword)
    score = compute_normalized_relevance(keyword_count, total_papers)

    return {
        "keyword_count": keyword_count,
        "total_papers": total_papers,
        "score": score
    }