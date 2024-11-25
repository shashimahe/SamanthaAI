import tool_functions
from groq import Groq
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from zoneinfo import ZoneInfo
import json, inspect

API_KEY = "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"
client = Groq(api_key=API_KEY)


def load_prompt(file):
    with open(file, "r") as f:
        content = f.read()
    return content

def get_tool_functions():
    """Retrieve name of all functions in the tool_functions module."""
    return {name: obj for name, obj in inspect.getmembers(tool_functions, inspect.isfunction)}
    
def get_tool_functions_description():
    """Retrieve descriptions of all functions in the tool_functions module."""
    return [inspect.getdoc(func) for _, func in inspect.getmembers(tool_functions, inspect.isfunction)]


prompt_file = "./initial_prompt.md"    
system_prompt = load_prompt(prompt_file)
tool_function_descriptions = str(get_tool_functions_description())
system = system_prompt + "Provided Tools\n" + tool_function_descriptions
tool_functions = get_tool_functions()
conversation = []

class UserRequest(BaseModel):
    query: str
    username: str = Field(default_factory="Shashi")
    created_at: str = Field(default_factory=lambda: datetime.now().strftime("%b %d, %Y %I:%M %p"))

    @field_validator("created_at", mode="before")
    def format_time(cls, value):
        if isinstance(value, datetime):
            return value.strftime("%b %d, %Y %I:%M %p")
        return value

def model(conversation):
    completion = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {
            "role": "system",
            "content": system
        },
        {
            "role": "user",
            "content": str(conversation)
        },
    ],
    temperature=0.5,
    max_tokens=1024,
    top_p=1,
    stream=False,
    response_format={"type": "json_object"},
    stop=None,
    )
    result = json.loads(completion.choices[0].message.content)
    while result.get("action") is not None:
        action = result.get("action")
        tool_name = action.get("tool_name")
        arguments = action.get("arguments")
        if tool_name in tool_functions:
            function = tool_functions[tool_name]
            observation = function(**arguments)
            conversation.append(observation)
            return model(conversation)
    return result

def response(query):
    request = UserRequest(query=query)
    conversation.append(request.model_dump_json())
    result = model(conversation)
    conversation.append(result)
    return result


print(response("list all files in current directory"))
