from fastapi import APIRouter, Depends, status
from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fast_bloge.core import token
from fast_bloge.models import model
from fast_bloge.models.database import get_db
from fast_bloge.models.database import rds
from fast_bloge.services.hash import Hash
from fast_bloge.tasks.task import create_user_ip

router = APIRouter(tags=['authentication'])


@router.post('/token')
def get_token(hosts: Request, request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid credential')
    if not Hash.verify(user.hashed_password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid password')
    block = rds.get(user.id)
    if block:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='blocked user')
    access_token = token.create_access_token(data={'sub': request.username})
    client = hosts.client.host
    username = request.username
    create_user_ip.delay(client, username)
    return {
        'access_token': access_token,
        'type_token': 'bearer',
        'username': user.username
    }
