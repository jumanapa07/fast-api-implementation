from pydantic import BaseModel,EmailStr
from datetime import datetime

class Token(BaseModel): 
    access_token: str 
    token_type: str 
    
class TokenData(BaseModel): 
    email : str | None = None 

class User(BaseModel): 
    email : str | None = None
    disabled : bool | None = None 
    
class UserInDB(User): 
    hashed_password : str 

class OTPModel(BaseModel): 
    email: EmailStr 
    otp: str 
    expires_at: datetime
