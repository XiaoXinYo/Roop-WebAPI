from flask import Flask, Response, request, send_file
from module import core, task, redis, auxiliary
import flask_apscheduler
import flask_cors
import config
import uuid

APP = Flask(__name__)
redis.init()
task.init()
APSCHEDULER = flask_apscheduler.APScheduler(app=APP)
flask_cors.CORS(APP, supports_credentials=True)

@APP.errorhandler(404)
def error404(error: Exception) -> Response:
    return core.GenerateResponse().error(404, 'not found page', httpCode=404)

@APP.errorhandler(500)
def error500(error: Exception) -> Response:
    return core.GenerateResponse().error(500, 'unknown error', httpCode=500)

@APP.post('/submit')
def submit() -> Response:
    target = request.files.get('target')
    source = request.files.get('source')
    parameter = core.getRequestParameter(request)
    modes = request.form.getlist('modes')
    keepFPS = parameter.get('keepFPS', False)
    skipAudio = parameter.get('skipAudio', False)
    manyFace = parameter.get('manyFace', False)
    if not target or not modes:
        return core.GenerateResponse().error(110, 'parameter cannot be empty')

    targetFormat = target.filename.split('.')[-1]
    if targetFormat not in ['png', 'jpg', 'mp4']:
        return core.GenerateResponse().error(110, 'the target file format is not supported')
    elif target.content_length > config.INPUT_FILE_MAX_SIZE * 1024:
        return core.GenerateResponse().error(110, 'the target file size exceeds the max limit')

    token = str(uuid.uuid4())
    if 'replace' in modes:
        if not source:
            return core.GenerateResponse().error(110, 'parameter cannot be empty')
        sourceFormat = source.filename.split('.')[-1]
        if sourceFormat not in ['png', 'jpg']:
            return core.GenerateResponse().error(110, 'the source file format is not supported')
        elif source.content_length > config.INPUT_FILE_MAX_SIZE * 1024:
            return core.GenerateResponse().error(110, 'the source file size exceeds the max limit')
        source.save(f'{config.INPUT_FOLDER_PATH}/{token}_source.{sourceFormat}')
    target.save(f'{config.INPUT_FOLDER_PATH}/{token}_target.{targetFormat}')
    redis.add(token, targetFormat, sourceFormat if source else None, modes, {
        'keepFPS': bool(keepFPS),
        'skipAudio': bool(skipAudio),
        'manyFace': bool(manyFace)
    })
    return core.GenerateResponse().success(token)

@APP.post('/delete')
def delete() -> Response:
    token = core.getRequestParameter(request).get('token')
    if not token:
        return core.GenerateResponse().error(110, 'parameter cannot be empty')

    task = redis.getTask(token)
    if not task:
        return core.GenerateResponse().error(120, 'task not found')
    if task['state'] == core.State.ING:
        return core.GenerateResponse().error(120, 'task is running')
    auxiliary.removeFile(f'{config.INPUT_FOLDER_PATH}/{token}_target.{task["targetFormat"]}')
    auxiliary.removeFile(f'{config.INPUT_FOLDER_PATH}/{token}_source.{task["sourceFormat"]}')
    auxiliary.removeFile(f'{config.OUTPUT_FOLDER_PATH}/{token}.{task["targetFormat"]}')
    redis.deleteQueue(token)
    redis.deleteTask(token)
    return core.GenerateResponse().success('success')

@APP.get('/get_state')
def get_state() -> Response:
    token = core.getRequestParameter(request).get('token')
    if not token:
        return core.GenerateResponse().error(110, 'parameter cannot be empty')

    task = redis.getTask(token)
    if not task:
        return core.GenerateResponse().error(120, 'task not found')
    return core.GenerateResponse().success(task['state'])

@APP.get('/download')
def download() -> Response:
    token = core.getRequestParameter(request).get('token')
    if not token:
        return core.GenerateResponse().error(110, 'parameter cannot be empty')

    task = redis.getTask(token)
    if not task:
        return core.GenerateResponse().error(120, 'task not found')
    if task['state'] == core.State.SUCCESS:
        return send_file(f'{config.OUTPUT_FOLDER_PATH}/{token}.{task["targetFormat"]}', as_attachment=True)
    return core.GenerateResponse().error(130, 'task cannot be downloaded')

@APSCHEDULER.task('interval', minutes=3)
def removeDoneTask() -> None:
    tasks = redis.getTasks()
    for task in tasks:
        if task['state'] == core.State.SUCCESS or task['state'] == core.State.FAIL:
            if auxiliary.getTimestamp() - task['timestamp'] > config.TASK_DONE_SAVE_TIME * 60:
                redis.deleteTask(task['token'])
                auxiliary.removeFile(f'{config.OUTPUT_FOLDER_PATH}/{task["token"]}.{task["targetFormat"]}')

if __name__ == '__main__':
    APSCHEDULER.start()
    APP.run(host=config.HTTP['host'], port=config.HTTP['port'], debug=True)