from sqlalchemy.orm.session import Session

from fast_bloge.user.hash import Hash
from fast_bloge.user.schemas import UserBase
from fast_bloge.user.models import User


def create_user(db: Session, request: UserBase):
    user = User(
        username=request.username,
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        hashed_password=Hash.bcrypt(request.password)

    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
