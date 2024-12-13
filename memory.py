import json

from models import *

class shortTermMemory:
    def __init__(self):
        self.content = []

    def update(self, conversation: conversationModel):
        self.content.append(conversation.model_dump_json())

    def load(self, n_conv):
        convs = self.content[-n_conv:]  # Fixed off-by-one error
        markdown_output = "# Recent converstaions\n"
        for entry in convs:
            record = json.loads(entry)
            user = record["user"]
            ai_response = record["ai"]
            markdown_output += f"{user['username']}: {user['query']}\n"
            markdown_output += f"AI: {ai_response}\n\n"
        return markdown_output
