import yaml

class AssistantPersona:
    def __init__(self, config_file):
        # Load the YAML configuration file
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)
        
        # Extract identity information
        identity = config.get('identity', {})
        self.name = identity.get('name', 'Unknown')
        self.age = identity.get('age', 'Unknown')
        self.gender = identity.get('gender', 'Unknown')
        self.ethnicity = identity.get('ethnicity', 'Unknown')
        
        # Extract personality traits
        personality = config.get('personality', {})
        self.traits = personality.get('traits', [])
        
        # Extract response style
        response_style = config.get('response_style', {})
        self.tone = response_style.get('tone', 'neutral')
        self.length = response_style.get('length', 'medium')
        self.formality = response_style.get('formality', 'formal')
        self.empathy_level = response_style.get('empathy_level', 'low')

    def create_prompt(self):
        # Create a system prompt using the imported variables
        system_prompt = f"""
        You are {self.name}, a {self.age}-year-old {self.gender} assistant with {self.ethnicity} background.
        You are known for being {', '.join(self.traits)}.
        Your responses are {self.tone}, {self.length}, {self.formality}, and show a {self.empathy_level} level of empathy).

        INSTRUCTIONS:
        Always maintain a {self.tone} and {self.formality} tone in your interactions.
        Keep responses {self.length}, ensuring they are {self.traits[3]} and {self.traits[2]}.
        Prioritize being {self.traits[0]} and {self.traits[1]} in every interaction.
        """
        return system_prompt
    