from functools import wraps
from typing import Annotated
from fastapi.security import  OAuth2PasswordRequestForm ,OAuth2PasswordBearer
from fastapi_mail import FastMail, MessageSchema
from fastapi import HTTPException,status,Depends
import random
import jwt
from jwt.exceptions import InvalidTokenError 
from passlib.context import CryptContext 
from datetime import timedelta,datetime,timezone
from config import conf
from .database import collection,otp_collection
from .models import Token,User,TokenData
from .schema import RegisterUser

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" 
ALGORITHM = "HS256" 
ACCESS_TOKEN_EXPIRE_MINUTES = 30 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def send_otp_decorator(func):
    @wraps(func)
    async def wrapper(user: User, otp: str, *args, **kwargs):
        email_message = MessageSchema(
            subject="OTP Code",
            recipients=[user.email],
            body=f"OTP: {otp}",
            subtype="html"
        )
        fm = FastMail(conf)
        await fm.send_message(email_message)
        return await func(user, otp, *args, **kwargs)
    return wrapper

def generate_otp_decorator(func):
    @wraps(func)
    async def wrapper(user: User, *args, **kwargs):
        otp_generated = generate_otp()
        return await func(user, otp_generated, *args, **kwargs)
    return wrapper

def send_email_decorator(func):
    @wraps(func)
    @generate_otp_decorator
    @send_otp_decorator
    async def wrapper(user: User, otp: str, *args, **kwargs):
        otp_collection.insert_one({"email":user.email, "otp":otp})
        return await func(user, *args, **kwargs)
    return wrapper

def generate_otp():
    return str(random.randint(10000, 99999))

def authenticate_user_decorator(func):
    @wraps(func)
    async def wrapper(form_data:Annotated[OAuth2PasswordRequestForm,Depends(RegisterUser)],*args, **kwargs):
        email = form_data.email 
        password=form_data.password
        user=collection.find_one({"email":email})
        if not user or user["disabled"]: 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not verified") 
        hashed_password=pwd_context.hash(password)
        if not  pwd_context.verify(password,hashed_password):
             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="password not verified") 
        kwargs["form_data"] =form_data
        data = {"sub": user["email"]} 
        kwargs["data"] = data
        return await func(*args, **kwargs) 
    return wrapper
    
def create_access_token_decorator(func):
    @authenticate_user_decorator
    @wraps(func)
    async def wrapper(data:dict,expires_delta:timedelta|None = None,*args,**kwargs): 
        to_encode = data.copy() 
        if expires_delta: 
            expire = datetime.now(timezone.utc) + expires_delta 
        else: 
            expire = datetime.now(timezone.utc) + timedelta(minutes = 15) 
        to_encode.update({"exp":expire}) 
        encoded_jwt= jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
        token=Token(access_token=encoded_jwt,token_type="bearer")
        kwargs['token']=token
        print(kwargs['token'])
        return await func(*args,**kwargs)
    return wrapper


def verify_token_decorator(func):
    @wraps(func)
    async def wrapper(token:str=Depends(oauth2_scheme),*args,**kwargs):
        credentials_exception = HTTPException( 
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"}, ) 
        try: 
            payload = jwt.decode(token,SECRET_KEY,ALGORITHM) 
            username : str = payload.get("sub") 
            if username is None: 
                raise credentials_exception 
            token_data=TokenData(username=username) 
        except InvalidTokenError: 
            raise credentials_exception 
        return func(token_data,*args,**kwargs)
    return wrapper
    
        


