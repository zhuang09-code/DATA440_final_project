import requests
from typing import List, Dict
from src.config import RESEARCH_URL

def get_papers(author_name: str) -> List[Dict]:
    """Get papers by author name using Semantic Scholar API."""
    
    # Step 1: Search for author
    try:
        res = requests.get(RESEARCH_URL, params={
            "query": author_name,
            "limit": 1
        })
        data = res.json()
    except Exception:
        return []

    authors = data.get("data")
    if not authors:
        return []

    author_id = authors[0].get("authorId")
    if not author_id:
        return []

    author_id = None

    for author in authors:
        name = (author.get("name") or "").lower()
        affiliations = " ".join(author.get("affiliations") or []).lower()
    
        if author_name.lower() in name and "william" in affiliations:
            author_id = author.get("authorId")
            break
        
    # Step 2: Get papers
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

def count_keyword(papers: List[Dict], keyword: str) -> int:
    """Count how many papers contain the keyword in title or abstract
    """
    count = 0
    keyword = keyword.lower()
    
    for p in papers:
        text = (p.get("title", "") + " " + (p.get("abstract") or "")).lower()
        
        if keyword in text:
            count += 1
            
    return count