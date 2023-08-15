HTTP = {
    'host': '0.0.0.0', # HTTP Host
    'port': 792, # HTTP Port
    'ssl': {
        'enable': False, # Enable HTTP SSL
        'keyPath': '', # HTTP SSL Key Path
        'certPath': '' # HTTP SSL Cert Path
    }
}

REDIS = {
    'host': '127.0.0.1', # Redis Host
    'port': 6379, # Redis Port
    'password': None, # Redis Password
    'db': 0 # Redis DB
}
REDIS_KEY_PREFIX = 'roop_webapi' # Redis Key Prefix

INPUT_FOLDER_PATH = './file/input' # Input Folder Path
OUTPUT_FOLDER_PATH = './file/output' # Output Folder Path
INPUT_FILE_MAX_SIZE = 30 # Single Input File Max Size,Unit: MB
TASK_DONE_SAVE_TIME = 60 * 24 # Task Done Save Time,Unit: Minute,Include Success Task(Output File),Fail Task.
ROOP_PYTHON_FILE_PATH = './venv/Scripts/python.exe' # Roop Python File Path
ROOP_FILE_PATH = './roop/run.py' # Roop File Path
TASK_THREAD_NUMBER = 1 # Task Thread Number
QUALITY = 18 # Quality,Only 1~100
MAX_MEMORY = 4 # Single Task Max Memory,Unit: GB
PROCESSOR = ['cpu'] # Processor,cpu,cuda for NATIVE,rocm for AMD(only Linux),dml for Windows,coreml for Mac
PROCESSOR_THREAD_NUMBER = 3 # Single Processor Max Thread Number