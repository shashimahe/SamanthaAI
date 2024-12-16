
from memory import shortTermMemory
from models import userRequestModel, conversationModel

from groq import Groq

class Model:
    def __init__(self):
        API_KEY = "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"
        self.client = Groq(api_key=API_KEY)

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
        response_format={"type": "json_object"},
        stop=None,
        )
        result = completion.choices[0].message.content
        return result
