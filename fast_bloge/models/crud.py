from sqlalchemy.orm.session import Session

from fast_bloge.models.database import rds
from fast_bloge.models.model import User, UserIP
from fast_bloge.models.schemas import BlockUser, UpdateUser, UserCreate
from fast_bloge.services.hash import Hash


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


def block_user(db: Session, request: BlockUser):
    user = db.query(User).filter(User.id == request.id).first()
    if user:
        rds.set(user.id, user.username)

    return "ok"


def user_ip(db: Session):
    return db.query(UserIP).all()