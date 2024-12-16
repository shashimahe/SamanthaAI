import subprocess
import json, threading, time
from duckduckgo_search import DDGS
from ytmusicapi import YTMusic

from basic_functions import *

def windows_terminal(command):
    """
    Executes a shell command in a terminal in windows OS
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
    

def android_terminal(command):
    """
    Execute a shell command in a terminal in android OS
    This tool can be used to do many actions in android smartphone
    It can be used to run termux api commands
    Some example termux api commands are
    "termux-torch on" - To turn on or off the smartphone torch.
    "termux-sms-list -n 5" - List last 5 SMS
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

'''
def android_ssh_terminal(command):
    """
    Execute a shell command in Termux Terminal in Android OS
    This tool can be used to do many actions in android phone
    It can be used to run termux api commands
    Some example termux api commands are
    "termux-torch on" - To turn on or off the smartphone torch.
    "termux-sms-list -n 5" - List last 5 SMS
    Args:
        command (str): The shell command to execute.
    """
    cmd = f"ssh -p 8022 u0_a294@192.168.93.55 '{command}'"
    return windows_terminal(cmd)
'''

def search_web(query, search_type):
    """
    Performs a web search using DuckDuckGo and returns relevant results.
    Use this tool to find the information that you generally not aware.
    Use this tool to find latest and updated information.
    Use this tool to find images, videos, music, news whenever user requested 
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


def play_music(audio_name):
    """
    Use this tool to play music, songs or any audios
    Args:
        audio_name (str): Name of the song, music or any audio you want to play
    """
    print(f">>> Searching {audio_name}....")
    yt = YTMusic()
    media_search = yt.search(query=audio_name, filter="songs", limit=2)
    data = media_search[:1]
    output = {}
    # Extracting useful details such as audio title, album, artists and audio url
    for item in data:
        output["Audio Name"] = item.get('title', 'No Title')
        output["Album"] = item.get('album', {}).get('name', 'No Album Name')
        output["Artists"] = [artist.get('name', 'Unknown Artist') for artist in item.get('artists', [])]
        video_id = item.get('videoId', 'No Duration')
        link = f"https://music.youtube.com/watch?v={video_id}"
    
    link = link

    def open_link(link):
            command = f'termux-open {link}'
            time.sleep(2)
            return android_terminal(command)
    
    openlink_thread = threading.Thread(target=open_link, args=(link,)).start()
    return f"{json_to_markdown(output)}\n Above audio is playing"

def open_link(link):
    """
    To open links or any url in Android OS Browser
    Remember, use this only when the OS is Android
    Args:
        link (str): URL or Link to open
    """
    command = f'termux-open {link}'
    time.sleep(2)
    return android_terminal(command)




