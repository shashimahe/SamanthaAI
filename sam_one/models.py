from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any
from datetime import datetime

class conversationModel(BaseModel):
    query: str = Field(description="Request from the User")
    ai: str = Field(description="Response from the AI")

class LLMPersonality(BaseModel):
    name: str = Field(default="Samantha", description="Name of the personal assistant.")
    age: int = Field(default=25, ge=18, le=100, description="Age of the assistant, must be realistic.")
    gender: Literal["Male", "Female", "Non-binary"] = Field(default="Female", description="Gender of the assistant.")
    nature: Literal["Introvert", "Extrovert", "Ambivert"] = Field(default="Extrovert", description="Nature or social orientation.")
    openness: Literal["Low", "Medium", "High"] = Field(default="Medium", description="Level of openness.")
    empathy: Literal["Low", "Medium", "High"] = Field(default="Medium", description="Level of empathy.")
    humor: Literal["Low", "Medium", "High"] = Field(default="Medium", description="Level of humor.")
    traits: list[str] = Field(default=["Attentive", "Caring"], description="Specific traits that describe the assistant.")
    tone: Literal["Formal", "Casual", "Professional"] = Field(default="Casual", description="Tone used in communication.")
    response_length: Literal["Short", "Medium", "Detailed"] = Field(default="Short", description="Preferred response length.")
