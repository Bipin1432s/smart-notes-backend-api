from pydantic import BaseModel, EmailStr
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str
class Login(BaseModel):
    email: str
    password: str
class NoteCreate(BaseModel):
    title: str = Field(..., min_length=3)
    content: str = Field(..., min_length=5)