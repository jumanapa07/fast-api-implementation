from pydantic import BaseModel,EmailStr
from typing import List

class User(BaseModel): 
    username : str
    email : str | None = None
    disabled : bool | None = None 
    
class UserInDB(User): 
    hashed_password : str 
    
