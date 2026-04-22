from numpy.char import title


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
