import subprocess
import json, pprint
from duckduckgo_search import DDGS

def RUN_SHELL_COMMAND(command):
    """
    Use this tool to executes shell commands and retrieves the output or error.
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
    Use this tool to Search for information from web or google. Information such as images, videos, news, maps, recent facts etc.
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