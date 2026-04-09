import requests
from typing import List, Dict
from src.config import RESEARCH_URL

def get_papers(author_name: str) -> List[Dict]:
    """Get papers by author name using Semantic Scholar API.
    """
    # Using semanticscholar API to search for the author and get their papers (googlescholar doesn't have an official API)
    url = RESEARCH_URL
    params = {
        "query": author_name,
        "limit": 1
    }
    
    res = requests.get(url, params=params)
    data = res.json()
    
    if not data["data"]:
        return []
    
    author_id = data["data"][0]["authorId"]
    
    # Collect papers for the authors
    papers_url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers"
    params = {
        "limit": 100,
        "fields": "title,abstract"
    }
    
    res = requests.get(papers_url, params=params)
    return res.json().get("data", [])

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