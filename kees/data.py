import os
import json
import datetime
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import InvalidToken


class KeesCrypt:
    def __init__(self, password, salt):
        key = self.generate_key(password.encode(), salt)
        self.fernet = Fernet(key)

    @classmethod
    def generate_key(cls, password, salt = None):
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
        return base64.urlsafe_b64encode(kdf.derive(password))

    def encrypt(self, data):
        return self.fernet.encrypt(data)

    def decrypt(self, data):
        return self.fernet.decrypt(data)

class KeesEntry(dict):
    def __init__(self, seq=None):
        dict.__init__(self)
        self.Title = ''
        self.UserName = ''
        self.Key = b''
        self.Salt = os.urandom(16)
        self.URL = ''
        self.Notes = ''
        self.CreationTime = datetime.datetime.now()
        self.ModificationTime = datetime.datetime.now()
        if seq:
            for (k, v) in seq.items():
                self[k] = v

    @property
    def Title(self):
        return self['title']

    @Title.setter
    def Title(self, title):
        self['title'] = title

    @property
    def UserName(self):
        return self['username']

    @UserName.setter
    def UserName(self, username):
        self['username'] = username

    @property
    def Key(self):
        return bytes.fromhex(self['key'])

    @Key.setter
    def Key(self, password):
        self['key'] = password.hex()

    @property
    def Salt(self):
        return bytes.fromhex(self['salt'])

    @Salt.setter
    def Salt(self, salt):
        self['salt'] = salt.hex() if salt else ''

    @property
    def URL(self):
        return self['url']

    @URL.setter
    def URL(self, url):
        self['url'] = url

    @property
    def Notes(self):
        return self['notes']

    @Notes.setter
    def Notes(self, notes):
        self['notes'] = notes

    @property
    def CreationTime(self):
        return datetime.datetime.strptime(self['creation'], '%Y%m%d %H%M%S')

    @CreationTime.setter
    def CreationTime(self, creation):
        self['creation'] = creation.strftime('%Y%m%d %H%M%S')

    @property
    def ModificationTime(self):
        return datetime.datetime.strptime(self['modification'], '%Y%m%d %H%M%S')

    @ModificationTime.setter
    def ModificationTime(self, modification):
        self['modification'] = modification.strftime('%Y%m%d %H%M%S')

    def setRawKey(self, key, password):
        self.Salt = os.urandom(16)
        crypt = KeesCrypt(password, self.Salt)
        self.Key = crypt.encrypt(key.encode())

    def getRawKey(self, password):
        crypt = KeesCrypt(password, self.Salt)
        return crypt.decrypt(self.Key).decode()

class KeesData(dict):
    def __init__(self, seq=None):
        dict.__init__(self)
        if seq:
            for (k, v) in seq.items():
                self[k] = KeesEntry(v)

    @classmethod
    def fromfile(cls, path, password):
        with open(path, mode = 'r') as f:
            js = json.loads(f.read())
            crypt = KeesCrypt(password, bytes.fromhex(js['s']))
            data = crypt.decrypt(bytes.fromhex(js['d']))
            return KeesData(json.loads(data.decode()))

    def save(self, path, password):
        with open(path, mode = 'w') as f:
            salt = os.urandom(16)
            crypt = KeesCrypt(password, salt)
            data = crypt.encrypt(json.dumps(self).encode())
            js = {}
            js['s'] = salt.hex()
            js['d'] = data.hex()
            f.write(json.dumps(js))

    def changePassword(self, password, old):
        for (k, v) in self.items():
            key = v.getRawKey(old)
            v.setRawKey(key, password)

def test_entry():
    entry = KeesEntry()
    entry.UserName = 'kylelaw'
    entry.setRawKey('123258', '123456')
    try:
        key1 = entry.getRawKey('fdsfds')
    except InvalidToken as a:
        pass
    entry.setRawKey('fdsfdsf', 'aaaa')
    key2 = entry.getRawKey('aaaa')

def test_save_load():
    data = KeesData.fromfile('e:\\testing.psw', '123456')


if __name__ == '__main__':
    test_entry()
    test_save_load()


