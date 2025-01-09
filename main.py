from datetime import datetime, timedelta, timezone 
from fastapi import FastAPI,Depends, HTTPException, status 
from pydantic import BaseModel 
from typing import List,Annotated 
import jwt 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from jwt.exceptions import InvalidTokenError 
from passlib.context import CryptContext 
from auth.routes import router as auth_router
from users.routes import router as user_router
app=FastAPI() 


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router,prefix="/user",tags=["user"])
    
    

@app.get("/")
def read_root():
    return {"message": "Welcome"}
    



