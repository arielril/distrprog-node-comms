from flask import current_app
from os import listdir
from os.path import isfile, isdir, join
from hashlib import sha256
import requests
import uuid


class Node():
    # resource => map['hash_id'] = 'file_name'
    resources = {}
    # endpoint of the supernode
    supernode_url = ''
    # uuid v4
    node_name = ''
    # node address
    location = ''

    def __init__(self, location: str, supernode: str):
        self.supernode_url = supernode
        self.node_name = str(uuid.uuid4())
        self.location = location

    def get_resources_for_registration(self):
        """
            [{
                "id": "<resource_id>",
                "name": "<resource_name>"
            }]
        """
        return list(map(
            lambda r: {
                'id': r[0],
                'name': r[1],
            },
            self.resources.items(),
        ))

    def register_to_supernode(self, app):
        try:
            req_data = {
                'name': self.node_name,
                'location': self.location,
                'resources': self.get_resources_for_registration(),
            }
            app.logger.info(
                f'[+] node ({self.node_name}) is registering.')

            res = requests.post(
                self.supernode_url + '/register',
                json=req_data,
                timeout=5,
            )

            if res.status_code == 204:
                app.logger.info(
                    f'[+] node ({self.node_name}) is registered')
            else:
                app.logger.warn(
                    f'[!] node ({self.node_name}) is not registered, something happend', res.status_code)
        except Exception as e:
            app.logger.error(
                f'[!] node ({self.node_name}) is not registered, request failed.', e)

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

    @classmethod
    def supernode_search_resource(cls, id: str):
        try:
            supernode_url = current_app.config['SUPERNODE_ENDPOINT']

            res = requests.get(
                '{}/search/{}'.format(supernode_url, id or ''),
            )

            if res.status_code != 200:
                current_app.logger.error(
                    f'[!] error searching for resource ({id}) at supernode')
                return None

            res_data = res.json()

            resource_info = None
            if 'data' in res_data \
                    and 'file' in res_data['data']:
                resource_info = res_data['data']['file']

            return resource_info
        except Exception as e:
            current_app.logger.error(
                f'[.] failed to search resource ({id}) at supernode.', e)
