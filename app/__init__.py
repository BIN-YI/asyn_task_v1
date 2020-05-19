from flask import Flask
from celery import Celery
#執行檔案得要absoute import
from app.recog.recog_func import RecogObj

#在這建立，可以直接啟動celery worker
#其實放外面或裡面意思是一樣，因為只有呼叫init_celery才啟動?!
#只能放在外面，因為若擺到init裡面，副程式結束就關閉
#這樣做是因為celery、flask都獨立運作(若採用flask celery套件則有所不同)
celery = Celery(__name__)
recog = RecogObj('recog')
#初始就要啟動辨識任務物件


def create_app(**kwargs):
    #flask instance
    app = Flask(__name__)

    #要給celery使用的config，MQ訊息佇列與Backend結果
    #flask app instance可呼叫config
    app.config['CELERY_BROKER_URL'] = 'amqp://cap:1234@23.97.66.207:5672/'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://:redisroot@23.97.66.207:6379/0'

    #register，blueprint註冊
    from .api import api
    from .recog_api import recog_api
    app.register_blueprint(api, url_prefix='/api/')
    app.register_blueprint(recog_api, url_prefix='/r_api/')

    #初始化celery
    init_celery(app)

    return app
#拆開，好處celery config設置上比較有彈性
def init_celery(app):

    #celery config setting
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']

    task_base = celery.Task
    #celery的任務context引入給flask，否則二者不認識
    class ContextTasks(task_base):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return task_base.__call__(self, *args, **kwargs)
    celery.Task = ContextTasks