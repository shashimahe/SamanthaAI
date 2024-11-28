import subprocess
import json, pprint
from duckduckgo_search import DDGS

def RUN_SHELL_COMMAND(command):
    """
    Tool Name: RUN_SHELL_COMMAND
    - Use this tool to executes shell commands and retrieves the output or error.
    Arguments: 
    - command (str): Command to run in yhe Bash Shell
    """
    try:
        print(f">>> Executing command: {command}")
        # Run the shell command and capture output
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
    - Use this tool to Search for information from web or google. Information such as images, videos, news, maps, recent facts etc.
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


a = SEARCH_WEB("current president of USA", "")
pprint.pprint(a)