from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import uuid4
from datetime import datetime
from enum import Enum
import json

def current_timestamp():
    return datetime.now().strftime("%d-%m-%Y %I:%M %p")

class taskModel(BaseModel):
    id: uuid4 = Field(default_factory=uuid4)
    name: str = Field(description="Name of the task")
    created_at: str = Field(default_factory=current_timestamp)
    due_at: Optional[str] = Field(description="Due date of the task (Format: ('%d-%m-%Y %I:%M %p'))")
    status: str = Field(description="Status of the Task: 'pending' or 'completed'")
    category: Optional[str] = Field(description="Cateogory of the Task: 'home', 'work'")
    priority: Optional[int] = Field(description="Assign Priority of the Task from 1 to 4 with 1 as high priority")
    project: Optional[str] = Field(default=None, description="Name of project that Task belongs to")
    tags: List[str] = Field(description="List of relavant tags to filter the task")


class noteModel(BaseModel):
    content: str = Field(description="Information to store in a note")
    note_type: str = Field(
        default="text",
        description="""
        Type of the note:
        text: Information is in normal text format
        list: Information is a list or points
        link: Information is a link or URL
        code: Information is a code snippet    
        """
        )
    tags: List[str] = Field(description="List of relavant tags to filter the task")

task = taskModel.model_json_schema()
note = noteModel.model_json_schema()
structure = json.dumps(note, indent="2")

print(structure)