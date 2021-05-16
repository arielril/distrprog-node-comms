from datetime import datetime


class Supernode():
    # entry => ['<file_hash>'] -> { file_name:str, node_location }
    node_resources = {}

    # entry => ['<node_location>'] -> { is_alive:bool, last_check:time }
    nodes = {}

    multicast_location = ''

    def __init__(self, multicast_loc=''):
        super().__init__()
        self.multicast_location = multicast_loc

    @classmethod
    def register_node(cls, location: str, resource_list):
        if not isinstance(resource_list, list):
            raise TypeError('`resource_list` must be a list')

        cls.nodes[location] = {
            'is_alive': True,
            'last_check': datetime.now(),
        }

        for r in resource_list:
            cls.node_resources[r['id']] = {
                'file_name': r['name'],
                'node_location': location,
            }

    @classmethod
    def get_resource_location(cls, id: str):
        if not id in cls.node_resources:
            # file doesn't exists here, need to search with the other supernodes
            return None

        return cls.node_resources[id]

    def multicasting(self):
        # https://pymotw.com/2/socket/multicast.html
        # https://stackoverflow.com/questions/603852/how-do-you-udp-multicast-in-python
        # https://gist.github.com/dksmiffs/96ddbfd11ad7349ab4889b2e79dc2b22
        pass
