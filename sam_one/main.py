from basic_functions import *
import my_tool_functions
import inspect
from memory import *
from llm import *
import json

model = Model()

# Retrieve function names and descriptions
tool_function_names = get_function_names(my_tool_functions)
tool_function_descriptions = get_function_descriptions(my_tool_functions)

assistant_personality = LLMPersonality()


context_prompt = f"""
Available Tools:
{json_to_markdown(tool_function_descriptions)}

System Details:
OS: Android
Date & Time: {current_timestamp()}
Username: Shashi

Assitant Details:
{assistant_personality}
"""

instructions_prompt = r"""
Understand the User Request and choose any one case to solve the problem
Case 1. If a tool is required to complete the request, determine the appropriate tool and arguments from the available tools and specify the tool name and required arguments in the below JSON format.
{
  "tool_name": "tool_name_here",
  "arguments": {
    "arg1": "value1",
    "arg2": "value2"
  }
}

Case 2. If it can be answered with your knowledge, prepare a response message in the below JSON format.
{"final_message": "Response Message to the user"}

NOTE: USE TOOLS ONLY IF NECESSARY
RESPONSE THE OUTPUT ONLY IN JSON FORMAT
"""


short_memory = shortTermMemory()

def Chat(query):
    instructions = f"Previous Conversations:\n{short_memory.load(5)}\n{context_prompt}\n{instructions_prompt}"
    ai_response= json.loads(model.Complete(instructions, query))
    if ai_response.get("tool_name"):
        tool_response = invoke_tool(tool_function_names, ai_response)
        memory = {"Query": query, "Tool Call": ai_response, "Tool Response": tool_response}
        update_query = f"""
        {json_to_markdown(memory)}
        Use above tool response as context and answer the query by constructing your response in final_message
        """
        return Chat(update_query)
    elif ai_response.get("final_message"):
        memory = {"Query": query, "AI Response": ai_response.get("final_message")}
        short_memory.update(memory)
        return ai_response.get("final_message")
    else:
        return "error"


if __name__ == "__main__":
    while True:
        query = input("Query:\n")
        result = Chat(query)
        print(result)

