import os
import hashlib

def getHash(filePath):

    if os.path.isfile(filePath):
        file_hash = hashlib.md5()
        with open(filePath, 'rb') as f:
            chunk = f.read(4096)
            while chunk:
                file_hash.update(chunk)
                chunk = f.read(4096)
        dhash=file_hash.hexdigest()
        return dhash
