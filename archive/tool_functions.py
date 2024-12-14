import subprocess
import json
from duckduckgo_search import DDGS

def RUN_SHELL_COMMAND(command):
    """
    Tool Name: RUN_SHELL_COMMAND
    Description: Executes a shell command in a terminal and returns the output or error.
    It can be used to run basic linux bash shell commands to handle the actions
    Args:
        command (str): The shell command to execute.
    """
    try:
        print(f">>> Executing command: {command}")
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if result.returncode == 0:
            return json.dumps({"status": "success", "output": result.stdout.strip()})
        else:
            return json.dumps({"status": "error", "error": result.stderr.strip()})
    except Exception as e:
        return json.dumps({"status": "error", "exception": str(e)})


def SEARCH_WEB(query, search_type):
    """
    Tool Name: SEARCH_WEB
    Description: Performs a web search using DuckDuckGo and returns relevant results.
    Args:
        query (str): The search term or keywords.
        search_type (str): Type of search:
            - "texts": General web results.
            - "answers": Direct answers to queries.
            - "images": Image search results.
            - "videos": Video search results.
            - "news": Latest news articles.
            - "maps": Location-based results.
    """
    with DDGS() as search:
        match search_type:
            case "texts":
                return search.text(query, max_results=2)
            case "answers":
                return search.answers(query)
            case "images":
                return search.images(query, region='wt-wt', safesearch='off', max_results=2)
            case "videos":
                return search.videos(query, region='wt-wt', safesearch='off', timelimit='y', max_results=2)
            case "news":
                return search.news(query, region='wt-wt', safesearch='off', timelimit='d', max_results=2)
            case "maps":
                return search.maps(query, place="Varthur", max_results=2)
