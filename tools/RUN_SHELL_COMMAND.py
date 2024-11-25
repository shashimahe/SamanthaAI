import subprocess
import json
import time
import threading
from ytmusicapi import YTMusic

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

