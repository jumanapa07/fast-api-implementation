from fastapi import APIRouter,Depends, HTTPException 
from .decorator import create_access_token_decorator,send_email_decorator
from .models import Token
from .schema import VerifyOTP,RegisterUser
from .database import collection,otp_collection
from passlib.context import CryptContext 
from fastapi.security import  OAuth2PasswordRequestForm 
from typing import Annotated

router=APIRouter() 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 

@router.post("/token")
@create_access_token_decorator
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends(RegisterUser)],token:Token = None)->Token:
    return token



@router.post("/register")
@send_email_decorator
async def register(user:RegisterUser):
    hashed_password= pwd_context.hash(user.password)
    collection.insert_one({"email": user.email, "hashed_password": hashed_password, "disabled": True})
    return {"detail": "OTP Sent Successfully"}

@router.post("/verify_otp")
async def verify(otp_data:VerifyOTP):
    stored_otp=otp_collection.find_one({"email":otp_data.email})
    if not stored_otp:
        raise HTTPException(status_code=400,detail="OTP not found")
    if stored_otp['otp'] != otp_data.otp:
        raise HTTPException(status_code=400,detail="Invalid OTP")
    collection.update_one({"email":otp_data.email},{"$set":{"disabled":False}})
    otp_collection.delete_one({"email": otp_data.email})
    return {"detail":"OTP Verified Succesfully"}


