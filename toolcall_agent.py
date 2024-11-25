import tool_functions
from groq import Groq
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from llm import Model
import json, inspect

API_KEY = "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"
client = Groq(api_key=API_KEY)

def load_prompt(file):
    with open(file, "r") as f:
        content = f.read()
    return content

def get_tool_functions_names():
    """Retrieve name of all functions in the tool_functions module."""
    return {name: obj for name, obj in inspect.getmembers(tool_functions, inspect.isfunction)}
    
def get_tool_functions_description():
    """Retrieve descriptions of all functions in the tool_functions module."""
    return [inspect.getdoc(func) for _, func in inspect.getmembers(tool_functions, inspect.isfunction)]


prompt_file = "./toolcall_prompt.md"    
tool_prompt = load_prompt(prompt_file)
tool_function_names = get_tool_functions_names()
tool_function_descriptions = get_tool_functions_description()
toolcall_prompt = tool_prompt + "Provided Tools" + str(tool_function_descriptions)

model = Model()

def Query(query):
    result = model.Query(toolcall_prompt, query)
    return result

if __name__ == "__main__":
    while True:
        user_input = input("Prompt:\n")
        result = Query(user_input)
        print(result)