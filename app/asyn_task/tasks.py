from .. import celery
from .. import recog
from ..recog import recog_func

#到時候會有張數計算
#這個每次都會產生一個新的self.id(很特別的機制)
@celery.task(bind=True)
def start_asyn_task(self):
    #辨識任務新增任務
    recog.add_short_task(self)

    #在任務物件裡面多放了一個task_list
    #之後可能該任務obj可以用此方式追蹤任務量
    #其他則是異步任務最終status，表示執行完畢
    return {'current': 100, 'total': 100, 'status': 'Task completed!', 'result': 'test success', "task_list": recog.task_list}

@celery.task(bind=True)
def start_asyn_task_long(self):
    #辨識任務新增任務
    recog.add_long_task(self)

    #在任務物件裡面多放了一個task_list
    #之後可能該任務obj可以用此方式追蹤任務量
    #其他則是異步任務最終status，表示執行完畢
    return {'current': 100, 'total': 100, 'status': 'Task completed!', 'result': 'test success'}