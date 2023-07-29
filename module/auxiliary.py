import time
import os

def getTimestamp(ms: bool=False) -> int:
    if ms:
        return int(time.time() * 1000)
    return int(time.time())

def removeFile(path: str) -> bool:
    if os.path.exists(path):
        os.remove(path)
        return True
    return False