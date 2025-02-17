import subprocess
import json, time
from ytmusicapi import YTMusic

from basic_functions import *

# Tool output should follow this json format {"tool_result": "output"}

def terminal(command):
    """
    Execute a shell command in a terminal in android OS
    This tool can be used to do many basic actions like
    "touch filename.txt" - To create a file
    "ls -l" - To list all files in the current directory
    It can also be used to run termux api commands
    Some example termux api commands are
    "termux-torch on" - To turn on or off the smartphone torch.
    "termux-sms-list" - List SMS
    Args:
        command (str): The shell command to execute.
    """
    try:
        print(f"Executing command: {command}")
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if result.returncode == 0:
            return {"result": "success", "output": result.stdout.strip()}
        else:
            return {"result": "error", "output": result.stderr.strip()}
    except Exception as e:
        return {"result": "error", "output": str(e)}


def play_music(audio_name):
    """
    This tool can be used to play music or songs 
    Args:
        audio_name (str): Name of the song, music or any audio you want to play. Default is Kannada Latest Hits
    """
    print(f"Searching {audio_name}....")
    yt = YTMusic()
    media_search = yt.search(query=audio_name, filter="songs", limit=2)
    data = media_search[:1][0]
  
    audio_name = data.get('title', 'No Title')
    album = data.get('album', {})
    artists = [artist.get('name', 'Unknown Artist') for artist in data.get('artists', [])]
    video_id = data.get('videoId', 'No Duration')
    url = f"https://music.youtube.com/watch?v={video_id}"           
    openlink_output = open_link(url)
    if openlink_output.get("result") == "error":
        return {"result": "error", "output": "Error while playing music"}
    return {"result": "success", "output": f"Playing {audio_name} from {album} by {artists}"}
    
def open_link(link):
    """
    This tool can be used to open links or any url in Android Browser
    Use this to open any link or url if user requested.
    Args:
        link (str): URL or Link to open
    """
    command = f'wslview {link}'
    terminal_output = terminal(command)
    if terminal_output.get("result") == "error":
        return {"result": "error", "output": "Error while opening link"}
    return {"result": "success", "output": "Provided link Opened Successfully"}
    