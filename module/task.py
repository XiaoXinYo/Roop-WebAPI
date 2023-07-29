from module import redis, core, auxiliary
import config
import threading
import time
import subprocess

LOCK = threading.Lock()

def init() -> None:
    for count in range(config.TASK_THREAD_NUMBER):
        threading.Thread(target=process).start()

def process() -> None:
    while True:
        LOCK.acquire()
        token = redis.queueDequeue()
        LOCK.release()
        if not token:
            time.sleep(10)
            continue

        redis.setTaskState(token, core.State.ING)
        task = redis.getTask(token)
        sourceFilePath = f'{config.INPUT_FOLDER_PATH}/{token}_source.{task["sourceFormat"]}' if task[
            'sourceFormat'] else None
        targetFilePath = f'{config.INPUT_FOLDER_PATH}/{token}_target.{task["targetFormat"]}'
        outputFilePath = f'{config.OUTPUT_FOLDER_PATH}/{token}.{task["targetFormat"]}'
        modes = task['modes']
        parameter = task['parameter']
        frameProcessor = []
        if 'replace' in modes:
            frameProcessor.append(f'face_swapper')
        if 'enhance' in modes:
            frameProcessor.append(f'face_enhancer')
        command = [
            config.PYTHON_FILE_PATH,
            config.ROOP_FILE_PATH,
            '-s', sourceFilePath if sourceFilePath else 'null',
            '-t', targetFilePath,
            '-o', outputFilePath,
            '--frame-processor', *frameProcessor,
            '--output-video-quality', str(config.QUALITY),
            '--max-memory', str(config.MAX_MEMORY),
            '--execution-provider', *config.PROCESSOR,
            '--execution-threads', str(config.PROCESSOR_THREAD_NUMBER)
        ]
        if parameter['keepFPS']:
            command.append('--keep-fps')
        if parameter['skipAudio']:
            command.append('--skip-audio')
        if parameter['manyFace']:
            command.append('--many-faces')
        try:
            result = subprocess.run(command, capture_output=True)
            if 'succeed' in result.stdout.decode('utf-8'):
                redis.setTaskState(token, core.State.SUCCESS)
            else:
                redis.setTaskState(token, core.State.FAIL)
        except:
            redis.setTaskState(token, core.State.FAIL)
        auxiliary.removeFile(f'{config.INPUT_FOLDER_PATH}/{token}_target.{task["targetFormat"]}')
        auxiliary.removeFile(f'{config.INPUT_FOLDER_PATH}/{token}_source.{task["sourceFormat"]}')