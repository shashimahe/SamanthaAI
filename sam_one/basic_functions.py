from datetime import datetime
import inspect
import json

from groq import Groq

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
        except:
            return json_data

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
        return json_data

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
                if tool_result.get("result") == "success":
                    return json_to_markdown(tool_result.get("output"))
            except Exception as e:
                return str(e)
        else:
            return f"Tool '{tool_name}' not found"
    return "No tool specified"

class Model:
    # Intiate model with response format, Use 'json' for JSON output
    def __init__(self, response_format=None):
        API_KEY = "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"
        self.client = Groq(api_key=API_KEY)
        if response_format == "json":
            self.response_format = {"type": "json_object"}
        else:
            self.response_format = response_format

    def Complete(self, system, user):
        completion = self.client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": user
            },
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        stream=False,
        response_format=self.response_format,
        stop=None,
        )
        result = completion.choices[0].message.content
        return result
