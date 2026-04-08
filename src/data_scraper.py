import requests

def get_papers(author_name):
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