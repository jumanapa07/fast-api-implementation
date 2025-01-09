# from functools import wraps

# from datetime import datetime, timedelta, timezone 
# from fastapi_mail import FastMail,MessageSchema
# from jwt.exceptions import InvalidTokenError 
# from passlib.context import CryptContext 
# from config import conf
# from .database import collection
# import random,jwt
# from .models import UserInDB


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" 
# ALGORITHM = "HS256" 
# ACCESS_TOKEN_EXPIRE_MINUTES = 30 



# async def verify_email(email:str):
#     user=collection.find_one({"email":email})
#     return user["disabled"] == False


# async def verify_password(plain_password,hashed_password):
#     return pwd_context.verify(plain_password,hashed_password) 

# async def get_password_hash(password):
#     return pwd_context.hash(password)

# async def get_user(email:str): 
#     user=collection.find_one({"email":email})
#     return user

# async def authenticate_user( email: str, password: str):
#     user=await get_user(email) 
#     if not user: 
#         return False 
#     if not await verify_password(password,user["hashed_password"]): 
#         return False 
#     if not await verify_email(email):
#         return False
#     return user 

# async def create_access_token(data:dict,expires_delta:timedelta|None = None): 
#     to_encode = data.copy() 
#     if expires_delta: 
#         expire = datetime.now(timezone.utc) + expires_delta 
#     else: 
#         expire = datetime.now(timezone.utc) + timedelta(minutes = 15) 
#     to_encode.update({"exp":expire}) 
#     encoded_jwt= jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM) 
#     return encoded_jwt 
    
# async def send_otp(email:str,otp:str):
#     email_message=MessageSchema(
#         subject="OTP  Code",
#         recipients=[email],
#         body=f"OTP: {otp}",
#         subtype="html"
#     )

#     fm=FastMail(conf)
#     await fm.send_message(email_message)

# def generate_otp():
#     return str(random.randint(10000,99999))

# async def send_email(email:str):
#     otp_generated=generate_otp()
    
#     await send_otp(email,otp_generated)
#     return otp_generated
    


    
# # 91888