from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    company_name: str
    document: str | None = None
    name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
