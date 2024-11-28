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
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
        )
        result = completion.choices[0].message.content
        return result