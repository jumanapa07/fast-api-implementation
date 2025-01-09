
from  pydantic import BaseModel,EmailStr
from typing import List


class RegisterUser(BaseModel): 
    email: EmailStr 
    password: str

class EmailSchema(BaseModel):
    email: List[EmailStr]

class VerifyOTP(BaseModel):
    email : EmailStr
    otp : str
    
