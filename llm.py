
from memory import shortTermMemory
from models import userRequestModel, conversationModel

from groq import Groq

class Model:
    def __init__(self):
        API_KEY = "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"
        self.client = Groq(api_key=API_KEY)

    def Query(self, context, request):
        completion = self.client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": context
            },
            {
                "role": "user",
                "content": request 
            },
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        #response_format={"type": "json_object"},
        stop=None,
        )
        result = completion.choices[0].message.content
        return result


def load_prompt(filename):
    filename = f"{filename}.md"
    try:
        with open(filename, "r") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return "File not found"


class Agent:

    def __init__(self, instructions):
        self.llm_model = Model()  # Ensure this class is implemented and functional
        self.instructions = load_prompt(instructions)  # Load the instructions saved in a markdown file
        self.short_term_memory = shortTermMemory()  # Initialize memory
        print("Welcome to your personal assistant chat! Type 'exit' to quit.")
    
    def chat(self, query):
        if query.lower() == "exit":
            print("Exiting the chat. Goodbye!")
            return None

        # Load recent memory, 5 conversations
        short_term_memory = self.short_term_memory.load(5)

        # Construct system prompt
        system = f"""
        {self.instructions}\n
        Recent Conversations:\n{short_term_memory}
        """

        # Create user request model
        user = userRequestModel(query=query)

        # AI model response with error handling
        try:
            ai = self.llm_model.Query(system, str(user))
        except Exception as e:
            ai = "Sorry, I encountered an issue processing your request."
            print(f"Error: {e}")

        # Update memory with the new conversation
        conv = conversationModel(user=user, ai=ai)
        self.short_term_memory.update(conv)

        # Display AI response
        return ai
