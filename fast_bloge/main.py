import logging

import sentry_sdk
import uvicorn
from celery import Celery
from fastapi import FastAPI

from fast_bloge.controller import autentication, sample
from fast_bloge.core.config import settings
from fast_bloge.core.main import create_app
from fast_bloge.models.database import Base, engine

sentry_sdk.init("https://7fb35b23b1fb4521bab620e0eeeceebe@sentry.mybitmax.com/12")
logger = logging.getLogger("uvicorn.error")

app: FastAPI = create_app()
app.include_router(sample.router)
app.include_router(autentication.router)
Base.metadata.create_all(engine)

@app.on_event("startup")
async def startup_event():
    for i in ["uvicorn.access", "uvicorn", "uvicorn.error"]:
        my_logger = logging.getLogger(i)
        if not my_logger:
            continue
        formatter = uvicorn.logging.ColourizedFormatter(
            "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] "
            "[trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
            , use_colors=False)
        if not len(my_logger.handlers):
            continue
        my_logger.handlers[0].setFormatter(formatter)


celery = Celery(
    __name__,
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=['fast_bloge.tasks'])

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8002)
