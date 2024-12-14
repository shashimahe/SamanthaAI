import tool_functions
import inspect
from memory import *


def get_tool_functions_names():
    """Retrieve names of all functions in the tool_functions module."""
    return {name: obj for name, obj in inspect.getmembers(tool_functions, inspect.isfunction)}

def get_tool_functions_description():
    """Retrieve descriptions of all functions in the tool_functions module."""
    return [inspect.getdoc(func) for _, func in inspect.getmembers(tool_functions, inspect.isfunction)]

# Retrieve function names and descriptions
tool_function_names = get_tool_functions_names()
tool_function_descriptions = get_tool_functions_description()

def load_prompt(filename):
    filename = f"{filename}.md"
    try:
        with open(filename, "r") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return "Persona file not found. Please define the assistant's persona."

tools_descriptions = ""
for entry in tool_function_descriptions:
    description = entry
    tools_descriptions += f"{description}\n"
