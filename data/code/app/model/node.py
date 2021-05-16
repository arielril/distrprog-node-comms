from os import listdir
from os.path import isfile, isdir, join
from hashlib import sha256
import requests


class Node():
    # resource => map['hash_id'] = 'file_name'
    resources = {}
    # endpoint of the supernode
    supernode_url = ''

    def __init__(self, supernode: str):
        self.supernode_url = supernode

    def register_to_supernode(self):
        try:
            res = requests.post(
                self.supernode_url + '/register',
                json={
                    'resources': [],
                    'node_name': 'my_beautiful_name',
                },
                timeout=5,
            )

            if not res.content is None:
                if res.status_code == 201:
                    print('[+] node is registered', res.json())
                else:
                    print(
                        '[!] node is not registered, something happend', res.content)
        except:
            print('[!] node is not registered, request failed')

    def load_resources(self, path=''):
        if not isdir(path):
            raise NotADirectoryError(f'"{path}" is not a directory')

        resource_files = [
            f for f in listdir(path) if isfile(join(path, f))
        ]

        for f in resource_files:
            self.resources[sha256(f.encode()).hexdigest()] = f

    @classmethod
    def list_resources(cls):
        return cls.resources

    @classmethod
    def get_resource(cls, id: str):
        if not id in cls.resources:
            return None
        return cls.list_resources()[id]
