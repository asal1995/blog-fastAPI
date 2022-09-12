from fastapi import APIRouter, Depends

from fast_bloge.models.database import get_db
from fast_bloge.user.schemas import UserBase
from fast_bloge.user import api

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/')
def create_user(user: UserBase, db=Depends(get_db)):
    return api.create_user(db, user)
