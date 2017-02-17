import os
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class KeesCrypto:
    def __init__(self, toppsw, deeppsw, salt = None):
        self.topkey = generate_key(toppsw.encode(), salt)
        self.deepkey = generate_key(deeppsw.encode(), self.topkey)

    @classmethod
    def generate_key(cls, password, salt = None):
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
        return base64.urlsafe_b64encode(kdf.derive(password))

    def encrypt(self, data, top):
        f = Fernet(self.topkey if top else self.deepkey)
        return f.encrypt(data)

    def decrypt(self, data, top):
        f = Fernet(self.topkey if top else self.deepkey)
        return f.decrypt(data)

class KeesEntry:
    def __init__(self):
        self.name = ""
        self.url = ""
        self.password = b''
        self.comment = ""

    def set_name(self, name):
        self.name = name

    def get_name(self, ):

class KeesData:
    def __init__(self):
        pass

    def load_from_file(self, path, password):
        pass

    def save_to_file(self, path, password):
        pass



def gen_key(password, salt):


Fernet.generate_key()
salt = os.urandom(16)
key = gen_key('123456789'.encode(), salt)
f = Fernet(key)
t = f.encrypt(b'lkdsjfildsfldskfdsjkf')

s = f.decrypt(t)

