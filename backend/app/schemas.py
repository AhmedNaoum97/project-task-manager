from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from typing import Literal
from datetime import datetime

class AuthSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=12, max_length=128, description="User's password")

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, v):
        if isinstance(v, str):
            return v.strip().lower()
        return v

class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(..., min_length=1, max_length=100, description="Title of the task")
    description: str | None = Field(default=None, max_length=2000)
    priority: Literal["low", "medium", "high"] = Field(default="medium", description="Priority of the task")
    due_date: datetime | None = None

class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    title: str = Field(default=None, min_length=1, max_length=100, description="Title of the task")
    description: str | None = Field(default=None, max_length=2000)
    status: Literal["pending", "in_progress", "completed"] = Field(default=None, description="Status of the task")        
    priority: Literal["low", "medium", "high"] = Field(default=None, description="Priority of the task")
    due_date: datetime | None = None

class LoginSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=1, max_length=128, description="User's password")

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, v):
        if isinstance(v, str):
            return v.strip().lower()
        return v