from flask import jsonify, request
from . import api
from ..tasks import long_count_tasks

@api.route('/test', methods=['POST'])
def make_test():
    data = request.get_json(force=True)
    task = long_count_tasks.delay(data['path'])
    return jsonify({"id": task.id})


@api.route('/status/<string:task_id>')
def take_status(task_id):
    task = long_count_tasks.AsyncResult(task_id)
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
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)