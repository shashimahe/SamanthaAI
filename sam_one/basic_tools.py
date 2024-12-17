import subprocess
import json, threading, time
from duckduckgo_search import DDGS
from ytmusicapi import YTMusic

from basic_functions import *


def terminal(command):
    """
    Execute a shell command in a terminal in android OS
    This tool can be used to do many basic actions like
    "touch filename.txt" - To create a file
    "ls -l" - To list all files in the current directory
    It can also be used to run termux api commands
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


def play_music(audio_name):
    """
    This tool can be used to play music or songs 
    Args:
        audio_name (str): Name of the song, music or any audio you want to play. Default is Kannada Latest Hits
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
        url = f"https://music.youtube.com/watch?v={video_id}"
        output["link"] = url
    
    audio_link = url

    command = f'termux-open {audio_link}'            
    open = terminal(command)
    if open.get("success") == True:
        output["Audio Status"] = "Playing"
        return output
    else:
        return {"Audio Status": "Failed to play"}

def open_link(link):
    """
    This tool can be used to open links or any url in Android Browser
    Use this to open any link or url if user requested.
    Args:
        link (str): URL or Link to open
    """
    command = f'termux-open {link}'
    open = terminal(command)
    if open.get("success") == True:
        return {"Open Link Status": "Opened"}
    else:
        return {"Open Link Status": "Failed"}




