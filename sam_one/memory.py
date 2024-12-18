from basic_functions import *

class shortTermMemory:
    def __init__(self):
        self.content = []

    def update(self, memory: dict):
        self.content.append(memory)

    def load(self, n_conv):
        convs = self.content[-n_conv:]
        return json_to_markdown(convs)
