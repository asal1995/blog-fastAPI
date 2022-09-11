from celery import Celery

from fast_bloge.core.config import get_settings

settings = get_settings()


def create_celery_app() -> Celery:
    app = Celery('fast_bloge',
                 broker=settings.redis_url,
                 backend=settings.redis_url,
                 include=['fast_bloge.tasks'])

    # Optional configuration, see the application user guide.
    app.conf.update(
        result_expires=3600,
    )
    app.conf.task_routes = {'me.*': {'queue': 'me'}, 'om.*': {'queue': 'om'}}
    return app


app = create_celery_app()
