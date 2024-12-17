from basic_functions import *
import basic_tools
from memory import *
import json

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

first_instructions = """
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

model = Model("json")
short_memory = shortTermMemory()

def firstAgent(query):
    system = f"""
    Previous Conversations:\n
    {short_memory.load(5)}\n
    {tools_prompt}\n
    {context_prompt}\n
    {first_instructions}
    """
    first_response = json.loads(model.Complete(system, query))
    return first_response

def secondAgent(action):
    if action.get("tool_name"):
      tool_result = invoke_tool(tool_names, action)
      if tool_result.get("success"):
        tool_output = tool_result.get("output")
        query = f"""
        Previous Conversations:\n
        {short_memory.load(5)}\n
        {tools_prompt}\n
        {context_prompt}\n
        For the following Query: "{query}"
        The tool output is as follows:
        {tool_output}
        Use the above tool output as context and answer the query by constructing your response in final_message json format.
        Json Format: {"response": "Response Message to the user"}
        """
        second_response = model.Complete("", query)
        return second_response
      else:
        return "error"
    else:
      return "error"
    
def mainAgent(query):
    first = firstAgent(query)
    if first.get("response"):
       mem = {"query": query, "action": "None", "response": first.get("response")}
       short_memory.update(mem)
       return first.get("response")
    else:
       second = secondAgent(first)
       if second.get("response"):
          mem = {"query": query, "action": first, "response": second.get("response")}
          short_memory.update(mem)
          return second.get("response")
       else:
          return "error"

if __name__ == "__main__":
    while True:
        query = input("Query:\n")
        result = mainAgent(query)
        print(result)

