import os
import hashlib


GET_DIR = ".ugit"

def init():
    os.makedirs (GET_DIR , exist_ok=True)
    os.makedirs(f'{GET_DIR}/objects' , exist_ok=True)

def hash_object(data , type_='blob'):
    obj = type_.encode() + b'\x00' + data
    oid = hashlib.sha1(obj).hexdigest()

    with open (f'{GET_DIR}/objects/{oid}','wb') as out:
        out.write(obj)
    
    return oid


def get_object(oid , expected='blob'):

    with open(f'{GET_DIR}/objects/{oid}', 'rb') as f:
        obj = f.read()
    
    type_ , _ , content = obj.partition(b'\x00')
    type_ = type_.decode()

    if expected is None:
        assert type_ == expected, f'Expected{expected} , got {type_}'
    return content

def set_HEAD(oid):
    with open(f'{GET_DIR}/HEAD', 'w') as f:
        f.write(oid)

def get_HEAD():
    if os.path.isfile(f'{GET_DIR}/HEAD'):
        with open(f'{GET_DIR}/HEAD') as f:
            return f.read().strip()
            
