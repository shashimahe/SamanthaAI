import tool_functions
import inspect
from memory import *
from llm import *
import json

def get_tool_functions_names():
    """Retrieve a dictionary of all functions in the tool_functions module."""
    return {name: obj for name, obj in inspect.getmembers(tool_functions, inspect.isfunction)}

def get_tool_functions_description():
    """Retrieve descriptions of all functions in the tool_functions module."""
    return {name: inspect.getdoc(func) for name, func in inspect.getmembers(tool_functions, inspect.isfunction)}

# Retrieve function names and descriptions
tool_function_names = get_tool_functions_names()
tool_function_descriptions = get_tool_functions_description()

tool_prompt = load_prompt("toolcall_prompt")

# Format tools' descriptions for instructions
tools_descriptions = "\n\n".join(
    f"{name}: {description}" for name, description in tool_function_descriptions.items()
)

tools_instructions = f"""
{tool_prompt}
Available Tools:
{tools_descriptions}
"""

def tool_agent(query):
    """Process a query using available tools."""
    tool_agent = Agent(tools_instructions, {"type": "json_object"})
    response = json.loads(tool_agent.chat(query))
    
    while response.get("tool_name"):
        tool_name = response["tool_name"]
        arguments = response.get("arguments", {})
        
        # Check if the tool exists
        if tool_name in tool_function_names:
            function = tool_function_names[tool_name]
            tool_result = function(**arguments)
            return tool_result
        else:
            return {"error": f"Tool '{tool_name}' not found."}
    
    return {"error": "No tool selected in the response."}

# Example query
query = "whoami"
print(tool_agent(query))