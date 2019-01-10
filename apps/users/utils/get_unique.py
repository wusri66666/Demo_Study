import hashlib
import uuid


def get_unique_str():
    unique_str = str(uuid.uuid4()).encode('utf-8')
    md5 = hashlib.md5()
    md5.update(unique_str)
    return md5.hexdigest()