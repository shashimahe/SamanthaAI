import pprint
from duckduckgo_search import DDGS

def SEARCH_WEB(query, search_type):
    """
    Tool Name: SEARCH_WEB
    - Use this tool to Search for information that doesn't comes under your knowledge. Such as images, videos, news, maps, recent facts etc.
    - This tool fetches information from the web and return results in JSON format
    Arguments:
    - query (str): The search term or phrase to look up.
    - search_type (str): The type of search to perform. Options include:
        - "texts": For general text-based search results.
        - "answers": For direct answers to queries.
        - "images": For image search results.
        - "videos": For video search results.
        - "news": For news articles.
        - "maps": For location-based search results.
    """
    with DDGS() as search:
        match search_type:
            case "texts":
                return search.text(query, region='in-en', max_results=5)
            case "answers":
                return search.answers(query)
            case "images":
                return search.images(query, region='wt-wt', safesearch='off', max_results=2)
            case "videos":
                return search.videos(query, region='wt-wt', safesearch='off', timelimit='y', max_results=2)
            case "news":
                return search.news(query, region='in-en', safesearch='off', timelimit='d', max_results=10)
            case "maps":
                return search.maps(query, place="Varthur, Bangalore", max_results=2)


a = SEARCH_WEB("Who won last T20 cricket World cup?", "news")
pprint.pprint(a)