from basic_functions import *
import basic_tools
from memory import *
from models import *
import json

# Create a Short Term Memory
short_memory = shortTermMemory()

# Retrieve function names and descriptions
tool_names = get_function_names(basic_tools)
tool_descriptions = get_function_descriptions(basic_tools)

# Tool function descriptions
tools_prompt = f"""
## Available Tools:
{json_to_markdown(tool_descriptions)}
"""

# ToolCall instructions
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

- Case 2. If it can be answered with your knowledge and no specific tool is required then prepare a output in the below JSON format.
{"response_message": "Final Response to the user"}

NOTE: USE TOOLS ONLY IF NECESSARY
RESPONSE THE OUTPUT ONLY IN JSON FORMAT
"""

# Contextual details
context_prompt = f"""
## System Details:
Date & Time: {current_timestamp()}
Username: Shashi
"""

# Assistant personality
persona_prompt = f"""
## Assistant Personality:
{assistantPersonality()}
"""

# Initiate LLM models
json_model = Model("json")
text_model = Model()

def firstAgent(query):
    short_memory_prompt = short_memory.load(5)
    system = f"""
    Previous Conversations:
    {short_memory_prompt}\n
    {context_prompt}\n
    {tools_prompt}\n
    {toolcall_instructions}\n
    """
    output = json.loads(json_model.Complete(system, query))
    return output


def toolResponseAgent(query, toolcall):
    short_memory_prompt = short_memory.load(3)
    if toolcall.get("tool_name"):
      tool_output = invoke_tool(tool_names, toolcall)
      query = f"""
      Previous Conversations:
      {short_memory_prompt}\n
      For the following
      Query: "{query}"
      Invoked Tool: {toolcall}
      Tool Output
      {tool_output}
      """ + """
      1. Understand and Analyse the Query and Tool Output after invoking the invoked tool
      2. Answer the user query in a short response message based on observation made from Query & Tool output.
      3. Response the output in following JSON format
      {"response_message": "Final Response to the user"}
      NOTE: OUTPUT ONLY IN JSON FORMAT
      """
      tool_response = json.loads(json_model.Complete("", query))
      return tool_response.get("response_message")
    else:
      return "Failed to get Tool Response"

def mainAgent(query):
    first_response = firstAgent(query)
    #print(first_response)
    if first_response.get("tool_name"):
        tool_response = toolResponseAgent(query, first_response)
        #print(tool_response)
        mem = {"Query": query, "Action": first_response, "AI Response": tool_response}
        short_memory.update(mem)
        return tool_response
    else:
        mem = {"Query": query, "Action": None, "AI Response": first_response.get("response_message")}
        short_memory.update(mem)
        return first_response.get("response_message")

if __name__ == "__main__":
    while True:
        query = input("Query:\n")
        result = mainAgent(query)
        print(result)

