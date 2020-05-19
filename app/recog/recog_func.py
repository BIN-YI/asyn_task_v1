import time
#任務的functions/modules，都放在這

#def example1():
class RecogObj():
    def __init__(self, name):
        self.name = name
        self.task_list = []
        self.count = 0
    #應該是一個人一個task，除非這task結束才有可能
    #所以確實這個recogObj得於最外面去initialization

    #這個設計成作為當前所有task_id list(之後混合的時候可以使用看看)
    def add_short_task(self, celery):
        self.count += 1
        #self.task_list.append(self.count)
        self.task_list.append(celery.request.id)
        self.short_update_test(celery)

    def add_long_task(self, celery):
        self.count += 1
        #self.task_list.append(self.count)
        self.task_list.append(celery.request.id)
        self.long_update_test(celery)

    def sleep_and_update(self, status, t, total, celery):
        i = status
        time.sleep(t)
        celery.update_state(state="PROGRESS",
                            meta={"current": i, "total": total, 'status': 'working'})

    def long_update_test(self, celery):

        self.sleep_and_update(10, 10, 100, celery)
        self.sleep_and_update(20, 10, 100, celery)
        self.sleep_and_update(35, 15, 100, celery)
        self.sleep_and_update(65, 20, 100, celery)
        self.sleep_and_update(85, 5,  100, celery)


    #update state測試，之後可以注入任何位置使用
    def short_update_test(self, celery):
        total = 100
        time.sleep(3)
        i = 30
        celery.update_state(state="PROGRESS",
                         meta={"current": i, "total": total, 'status': 'working'})
        time.sleep(3)
        i = 50
        celery.update_state(state="PROGRESS",
                        meta = {"current": i, "total": total, 'status': 'working'})

    #json回傳測試
    def recog_test(self):
        return {'state': 'success'}

class RecogTask():
    def __init__(self, task_id):
        self.task_id = task_id
    def long_count_tasks(s, total):
        total = int(total)
        for i in range(total):
            if i % 10 == 0:
                #到時候就要求辨識那邊程式，用這個來更新狀態
                #我這邊只做結束訊息
                s.update_state(state='PROGRESS',
                                  meta={'current': i, 'total': total, 'status': 'working'})
            time.sleep(1)
        #part 1
        # total數量可能是the number of parts in pipeline
        # current則是看目前所在區塊
        #s.update_state(state='PROGRESS', meta={'current': i, 'total': total, 'status': 'working'})

        #part 2
        # s.update_state(state='PROGRESS', meta={'current': i, 'total': total, 'status': 'working'})

        #...  dd