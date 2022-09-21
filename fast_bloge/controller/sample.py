

from typing import List

from fastapi import APIRouter, Depends
from fastapi.security.api_key import APIKey

from fast_bloge.core import token
from fast_bloge.models import crud
from fast_bloge.models.database import get_db
from fast_bloge.models.schemas import BlockUser, UpdateUser, UserBase, UserCreate

route = APIRouter()
router = APIRouter(prefix='/user', tags=['user'])


@router.post('/', response_model=UserBase)
def create_user(user: UserCreate, db=Depends(get_db)):
    return crud.create_user(db, user)


@router.get('/', response_model=List[UserBase])
def list_user(db=Depends(get_db)):
    return crud.list(db)


@router.get('/{id}', response_model=UserBase)
def get_user(id: int, db=Depends(get_db)):
    return crud.get_user(id, db)


@router.post('/delete/{id}')
def delete_user(id: int, db=Depends(get_db), token: str = Depends(token.oath2_schema)):
    return crud.delete_user(id, db)


@router.patch('/update/{id}')
def update_user(id: int, user: UpdateUser, db=Depends(get_db), token: str = Depends(token.oath2_schema)):
    return crud.update_user(id, db, user)


@router.post('/block/', )
def block_user(user: BlockUser, db=Depends(get_db), api_key: APIKey = Depends(token.get_api_key)):
    return crud.block_user(db, user)


@router.get("/ip/")
def ip_list(db=Depends(get_db)):
    return crud.user_ip(db)
