from flask import jsonify, request
#非執行，可以relative import
from . import recog_api
from .. import recog
from ..asyn_task.tasks import start_asyn_task, start_asyn_task_long
from .. import celery
from celery.result import AsyncResult

def on_raw_message(body):
    print(body)

#測試blueprint與postman用
@recog_api.route('/test_r', methods=['POST'])
def hello_test_r():
    return jsonify({"greeting": "Hello Recog"})

@recog_api.route('/test_roc', methods=['POST'])
def recog_obj_call():
    result = recog.recog_test()
    return jsonify(result)

#發動異步任務，取得異步任務最終return以及task_id
@recog_api.route('/task_id_result', methods=['POST'])
def task_id_result():
    task = start_asyn_task.apply_async()
    task_id = task.task_id

    #但這個結果，就得等待到異步任務完全執行完畢才能取得
    res = start_asyn_task.AsyncResult(task_id)
    r = res.get()

    return jsonify({'id': task_id,'result': r})


#發動異步任務，只取得task_id
@recog_api.route('/task_id', methods=['POST'])
def task_id():
    #可以快速取得task_id，因為他就發出任務，然後產生物件以及他的task_id
    task = start_asyn_task_long.apply_async()
    task_id = task.task_id

    return jsonify({'id': task_id})


#輸入task_id則可查詢
#<string: task_id>意思同於methods=['GET']
@recog_api.route('/status/<string:task_id>')
def take_status(task_id):
    #這邊萬一輸入錯的id怎麼辦，不就查不到!?!?
    task = start_asyn_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        #最後這個就是PROGRESS，他這種寫法是把特殊案例都列在上面(應該算是種習慣)
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': task.info.get('current'),
            'total': task.info.get('total'),
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)