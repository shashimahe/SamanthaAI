from llm import Model
from memory import shortTermMemory
from models import *

def load_prompt(filename):
    filename = f"{filename}.md"
    with open(filename, "r") as f:
        content = f.read()
    return content

if __name__ == "__main__":
    llm_model = Model()  # Uncomment and define Model if available
    persona = load_prompt("persona")
    short_term_memory = shortTermMemory()
    while True:
        # Load recent memory
        load_memory = short_term_memory.load(5)  # Fetch last 5 conversations
        system = f"""
        {persona}\n
        Use the below previous conversations as context only if required to answer the user's further requests.
        {load_memory}        
        """
        # User input
        query = input("Prompt: ")
        user = userRequestModel(query=query)
        # AI model response (placeholder)
        ai = llm_model.Query(system, str(user))
        # Update memory with the new conversation
        conv = conversationModel(user=user, ai=ai)
        short_term_memory.update(conv)

        # Display AI response
        print(f"AI Response: {ai}")
