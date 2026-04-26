import requests
from typing import List, Dict
from src.config import RESEARCH_URL

def get_papers(author_name: str, dept: str = "", interests: str = "") -> List[Dict]:
    """Get papers by author name using Semantic Scholar API with improved matching."""

    try:
        res = requests.get(RESEARCH_URL, params={
            "query": author_name,
            "limit": 10
        })
        data = res.json()
    except Exception:
        return []

    authors = data.get("data")
    if not authors:
        return []

    best_score = -1
    best_author = None

    # Clean name: "Last, First" → ["first", "last"]
    parts = author_name.lower().replace(",", "").split()
    if len(parts) >= 2:
        first = parts[1]
        last = parts[0]
    else:
        first = parts[0]
        last = parts[0]

    for author in authors:
        score = 0

        name = (author.get("name") or "").lower()
        affiliations = " ".join(author.get("affiliations") or []).lower()

        # Strong name match
        if first in name and last in name:
            score += 5
        elif last in name:
            score += 2
        else:
            score -= 3  # penalize wrong last name

        # Affiliation bonus
        if "william" in affiliations or "mary" in affiliations:
            score += 3

        # Interest matching (if available)
        if interests:
            if any(word in name for word in interests.lower().split()):
                score += 1

        if score > best_score:
            best_score = score
            best_author = author

    # Confidence check (helps with identifying issues that may come from scraping the semantic scholar website)
    if best_score < 3 or not best_author:
        print(f"⚠️ Low confidence match for {author_name}")
        return []

    author_id = best_author.get("authorId")

    print(f"{author_name} → selected: {best_author.get('name')} | score: {best_score}")
    print(f"Profile: https://www.semanticscholar.org/author/{author_id}")

    try:
        res = requests.get(
            f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers",
            params={
                "limit": 100,
                "fields": "title,abstract"
            }
        )
        papers_data = res.json()
    except Exception:
        return []

    return papers_data.get("data", [])