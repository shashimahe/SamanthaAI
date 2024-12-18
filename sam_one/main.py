from basic_functions import *
import basic_tools
from memory import *
import json

# Create a Short Term Memory
short_memory = shortTermMemory()

# Retrieve function names and descriptions
tool_names = get_function_names(basic_tools)
tool_descriptions = get_function_descriptions(basic_tools)

tools_prompt = f"""
## Available Tools:
{json_to_markdown(tool_descriptions)}
"""

context_prompt = f"""
## System Details:
OS: Android
Date & Time: {current_timestamp()}
Username: Shashi
"""

toolcall_instructions = """
## Instructions:
Understand the User Request and choose any one case to solve the problem
- Case 1. If a tool is required to complete the request, determine the appropriate tool and arguments from the available tools and specify the tool name and required arguments in the below JSON format.
{
  "tool_name": "tool_name_here",
  "arguments": {
    "arg1": "value1",
    "arg2": "value2"
  }
}
- Case 2. If it can be answered with your knowledge, prepare a response message in the below JSON format.
{"response": "Response Message to the user"}

NOTE: USE TOOLS ONLY IF NECESSARY
RESPONSE THE OUTPUT ONLY IN JSON FORMAT
"""

json_model = Model("json")
text_model = Model()

def toolCallAgent(query):
    system = f"""
    {tools_prompt}\n
    {context_prompt}\n
    {toolcall_instructions}
    """
    toolcall = json.loads(json_model.Complete(system, query))
    return toolcall


def toolResponseAgent(query, toolcall):
    if toolcall.get("tool_name"):
      tool_result = invoke_tool(tool_names, toolcall)
      if tool_result.get("tool_result"):
        tool_output = tool_result.get("output")
        query = f"""
        For the following
        Query: "{query}"
        Invoked Tool: {toolcall}
        Tool Output
        {tool_output}
        """ + """\n
        Understand and Analyse the Query and Tool Output after invoking the invoked tool
        Construct a short response message based on observation made from Query & Tool output.
        """
        tool_response = text_model.Complete("", query)
        return tool_response
      else:
        return "Failed to get Tool Response"
    else:
      return "No Tool found to invoke"
    
def mainAgent(query):
    tool_call = toolCallAgent(query)
    if tool_call.get("tool_name"):
        tool_response = toolResponseAgent(query, tool_call)
        mem = {"Query": query, "Tool Response": tool_response}
        short_memory.update(mem)
        return short_memory.load(5)
    else:
        mem = {"Query": query, "Tool Response": tool_call.get("response")}
        short_memory.update(mem)
        return short_memory.load(5)

if __name__ == "__main__":
    while True:
        query = input("Query:\n")
        result = mainAgent(query)
        print(result)

