from llm import Model
from memory import shortTermMemory
from models import *

def load_prompt(filename):
    filename = f"{filename}.md"
    try:
        with open(filename, "r") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return "Persona file not found. Please define the assistant's persona."

def chat():
    llm_model = Model()  # Ensure this class is implemented and functional
    persona = load_prompt("persona")  # Load persona description
    short_term_memory = shortTermMemory()  # Initialize memory
    print("Welcome to your personal assistant chat! Type 'exit' to quit.")
    while True:
        query = input("You: ")  # Get user input dynamically
        if query.lower() == "exit":
            print("Exiting the chat. Goodbye!")
            break
        # Load recent memory
        load_memory = short_term_memory.load(5)  # Fetch last 5 conversations      
        # Construct system prompt
        system = f"""
        {persona}\n
        Use the below previous conversations as context only if required to answer the user's further requests.
        {load_memory}
        """
        # Create user request model
        user = userRequestModel(query=query)

        # AI model response with error handling
        try:
            ai = llm_model.Query(system, str(user))
        except Exception as e:
            ai = "Sorry, I encountered an issue processing your request."
            print(f"Error: {e}")

        # Update memory with the new conversation
        conv = conversationModel(user=user, ai=ai)
        short_term_memory.update(conv)

        # Display AI response
        print(f"AI Response: {ai}")

if __name__ == "__main__":
    while True:
        chat()