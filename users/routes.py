from fastapi import APIRouter,Depends,HTTPException
from typing import Annotated

router=APIRouter() 






# @router.get("\me",response_model=User)
# async def get_user_me(current_user:Annotated[User,Depends(get_current_user)]):
#     return current_user


# @router.put("\me",response_model=User)
# async def update_user_me(update_user:User,current_user:Annotated[User,Depends(get_current_user)]):
#     current_user.update(update_user)
#     return current_user


