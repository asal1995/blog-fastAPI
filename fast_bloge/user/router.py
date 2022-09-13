from typing import List

from fastapi import APIRouter, Depends
from fastapi.security.api_key import APIKey

from auth import auth as _auth
from auth.oauth2 import oath2_schema
from fast_bloge.models.database import get_db
from fast_bloge.user import api
from fast_bloge.user.schemas import UserCreate, UserBase, UpdateUser, BlockUser

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/', response_model=UserBase)
def create_user(user: UserCreate, db=Depends(get_db)):
    return api.create_user(db, user)


@router.get('/', response_model=List[UserBase])
def list_user(db=Depends(get_db)):
    return api.list(db)


@router.get('/{id}', response_model=UserBase)
def get_user(id: int, db=Depends(get_db)):
    return api.get_user(id, db)


@router.post('/delete/{id}')
def delete_user(id: int, db=Depends(get_db), token: str = Depends(oath2_schema)):
    return api.delete_user(id, db)


@router.patch('/update/{id}')
def update_user(id: int, user: UpdateUser, db=Depends(get_db), token: str = Depends(oath2_schema)):
    return api.update_user(id, db, user)


# # Lockedown Route
# @router.get("/secure")
# async def info(api_key: APIKey = Depends(_auth.get_api_key)):
#     return {
#         "default variable": api_key
#     }
#
#
# # Open Route
# @router.get("/open")
# async def info():
#     return {
#         "default variable": "Open Route"
#     }


@router.post('/block/', )
def block_user(user: BlockUser, db=Depends(get_db), api_key: APIKey = Depends(_auth.get_api_key)):
    return api.block_user(db, user)
