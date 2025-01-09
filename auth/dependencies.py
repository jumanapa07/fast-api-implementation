from .database import collection
from .models import TokenData
from .decorator import verify_token_decorator

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" 
ALGORITHM = "HS256" 
ACCESS_TOKEN_EXPIRE_MINUTES = 30 


@verify_token_decorator
async def get_current_user(token_data:TokenData):  
    user = user=collection.find_one({"email":token_data.email})
    return user 

