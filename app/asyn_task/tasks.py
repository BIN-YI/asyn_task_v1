from .. import celery
from ..recog import recog_func

@celery.task(bind=True)
def start_asyn_task(self, total):
    #total
    recog_func.long_count_tasks(self, total)
    #函數結束，則回傳結束訊息
    return {'current': total,   otal': total, 'status': 'Task completed!', 'result': 'test success'}