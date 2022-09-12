from sqlalchemy.orm.session import Session

from fast_bloge.user.hash import Hash
from fast_bloge.user.schemas import UserCreate, UpdateUser
from fast_bloge.user.models import User


def create_user(db: Session, request: UserCreate):
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


def list(db: Session):
    return db.query(User).all()


def get_user(id, db: Session):
    user = db.query(User).filter(User.id == id).first()
    return user


def delete_user(id, db: Session):
    user = get_user(id, db)
    db.delete(user)
    db.commit()
    return 'ok'


def update_user(id, db: Session, request: UpdateUser):
    user = db.query(User).filter(User.id == id)
    user.update({
        User.username: request.username,
    }

    )
    db.commit()

    return "ok"
