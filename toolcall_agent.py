import tool_functions
import inspect
from memory import longTermMemory

def get_tool_functions_names():
    """Retrieve names of all functions in the tool_functions module."""
    return [name for name, _ in inspect.getmembers(tool_functions, inspect.isfunction)]

def get_tool_functions_description():
    """Retrieve descriptions of all functions in the tool_functions module."""
    return [inspect.getdoc(func) for _, func in inspect.getmembers(tool_functions, inspect.isfunction)]

# Retrieve function names and descriptions
tool_function_names = get_tool_functions_names()
tool_function_descriptions = get_tool_functions_description()

# Update long-term memory with the function details
tool_memory = longTermMemory("tools")
#a = tool_memory.UpdateMemory(tool_function_descriptions, tool_function_names)

b = tool_memory.RetreiveMemory("run shell command")
# Print the result of the memory update
print(b)
