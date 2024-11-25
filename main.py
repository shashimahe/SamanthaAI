
from prompts import AssistantPersona

assistant = AssistantPersona("./assistant_config.yaml")
assistant_persona_prompt = assistant.create_prompt()

