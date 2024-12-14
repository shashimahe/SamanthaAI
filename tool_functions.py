import subprocess
import json
from duckduckgo_search import DDGS

def ubuntu_terminal(command):
    """
    Tool Name: ubuntu_terminal
    Description: Executes a shell command in a terminal and returns the output or error.
    It can be used to run basic linux bash shell commands to handle basic actions 
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

def termux_terminal(command):
    """
    Tool Name: termux_terminal
    Description: Execute a shell command in Termux Terminal.
    It can be used to run termux api commands
    Eg:
    "termux-torch on" - To turn on or off the smartphone torch.
    "termux-sms-list -n 5 - To read sms
    Args:
        command (str): The shell command to execute.
    """
    cmd = f"ssh -p 8022 u0_a294@192.168.93.55 '{command}'"
    return ubuntu_terminal(cmd)

def search_web(query, search_type):
    """
    Tool Name: search_web
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
