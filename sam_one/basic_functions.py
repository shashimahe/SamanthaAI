from datetime import datetime
import inspect
import json

import my_tool_functions

def current_timestamp():
    return datetime.now().strftime("%d-%m-%Y %I:%M %p")

def json_to_markdown(json_data):
    """
    Converts JSON data to a neatly formatted Markdown string.

    :param json_data: JSON object or string
    :return: Markdown-formatted string
    """
    if isinstance(json_data, str):
        try:
            json_data = json.loads(json_data)
        except json.JSONDecodeError as e:
            return f"Error decoding JSON: {e}"

    def format_dict(data, indent=0):
        markdown = ""
        for key, value in data.items():
            markdown += f"{'  ' * indent}- {key}: "
            if isinstance(value, dict):
                markdown += "\n" + format_dict(value, indent + 1)
            elif isinstance(value, list):
                markdown += "\n" + format_list(value, indent + 1)
            else:
                markdown += f"{value}\n"
        return markdown

    def format_list(data, indent=0):
        markdown = ""
        for item in data:
            if isinstance(item, dict):
                markdown += f"{'  ' * indent}- \n" + format_dict(item, indent + 1)
            elif isinstance(item, list):
                markdown += f"{'  ' * indent}- \n" + format_list(item, indent + 1)
            else:
                markdown += f"{'  ' * indent}- {item}\n"
        return markdown

    if isinstance(json_data, dict):
        return format_dict(json_data)
    elif isinstance(json_data, list):
        return format_list(json_data)
    else:
        return "Unsupported JSON format."

def get_function_names(module_name):
    """Retrieve a dictionary of all functions in the tool_functions module."""
    return {name: obj for name, obj in inspect.getmembers(module_name, inspect.isfunction)}

def get_function_descriptions(module_name):
    """Retrieve descriptions of all functions in the tool_functions module."""
    return {name: inspect.getdoc(func) for name, func in inspect.getmembers(module_name, inspect.isfunction)}

def invoke_tool(tool_names, response):
    """Executes the requested tool from given tool_functions and returns its output in Markdown format."""
    while response.get("tool_name"):
        tool_name = response["tool_name"]
        arguments = response.get("arguments", {})
        if tool_name in tool_names:
            function = tool_names[tool_name]
            try:
                print(f"Running..{tool_name}({arguments})")
                tool_result = function(**arguments)
                return json_to_markdown(tool_result)
            except Exception as e:
                return {"success": False, "error": str(e)}
        else:
            return {"success": False, "error": f"Tool '{tool_name}' not found"}
    return {"success": False, "error": "No tool specified"}
