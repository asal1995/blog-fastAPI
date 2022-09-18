from fast_bloge.core.config import get_redis
from fast_bloge.task_manager import app

r = get_redis().__next__()


@app.task(name="me.getSampleList")
def get_order_list():
    return service_order.get_sample_list(r)


