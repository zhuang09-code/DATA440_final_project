import requests
from src.scrape_ds import scrape_ds

def get_papers(author_name):
    """Get papers by author name using Semantic Scholar API.
    """
    url = "https://api.semanticscholar.org/graph/v1/author/search"
    params = {
        "query": author_name,
        "limit": 1
    }
    
    res = requests.get(url, params=params)
    data = res.json()
    
    if not data["data"]:
        return []
    
    author_id = data["data"][0]["authorId"]
    
    # get papers
    papers_url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}/papers"
    params = {
        "limit": 100,
        "fields": "title,abstract"
    }
    
    res = requests.get(papers_url, params=params)
    return res.json().get("data", [])

def count_keyword(papers, keyword):
    """Count how many papers contain the keyword in title or abstract.
    """
    count = 0
    keyword = keyword.lower()
    
    for p in papers:
        text = (p.get("title", "") + " " + (p.get("abstract") or "")).lower()
        
        if keyword in text:
            count += 1
            
    return count