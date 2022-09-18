from fastapi import Depends

from fast_bloge.models.database import get_db
from fast_bloge.tasks.celery_worker import celery
from fast_bloge.user.models import UserIP


@celery.task()
def create_user_ip(client, username,  db=Depends(get_db)):
    ip = UserIP(
        username=username,
        ip=client
    )
    return 'ok'
