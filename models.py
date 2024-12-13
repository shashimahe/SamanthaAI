from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

def current_timestamp():
    return datetime.now().strftime("%d-%m-%Y %I:%M %p")

class userRequestModel(BaseModel):
    query: str = Field(description="Request from the User")
    username: str = Field(default="Shashi", description="Name of the User")
    #timestamp: str = Field(default_factory=current_timestamp)

class conversationModel(BaseModel):
    user: userRequestModel = Field(description="Request from the User")
    ai: str = Field(description="Response from the AI")