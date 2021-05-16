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
    def register_node(cls, location: str, resource_list, name='') -> (bool, Exception):
        if not isinstance(resource_list, list):
            return False, TypeError('node `resources` must be a list')

        if len(resource_list) == 0:
            # ignore nodes without resources, just gabage
            return True, None

        cls.nodes[location] = {
            'is_alive': True,
            'last_check': datetime.now(),
            'name': name,
        }

        for r in resource_list:
            cls.node_resources[r['id']] = {
                'file_name': r['name'],
                'node_location': location,
            }

        return True, None

    @classmethod
    def get_resource_location_by_id(cls, id: str):
        if not id in cls.node_resources:
            # file doesn't exists here, need to search with the other supernodes
            """
            return format
                [{
                    "id": "<file_id>",
                    "file": {
                        "name": "<file_name>",
                        "location": "<file_location>"
                    }
                }]
            """
            return None

        file_info = cls.node_resources[id]
        return {
            'id': id,
            'file': {
                'name': file_info['file_name'],
                'location': file_info['node_location'],
            },
        }

    def multicasting(self):
        # https://pymotw.com/2/socket/multicast.html
        # https://stackoverflow.com/questions/603852/how-do-you-udp-multicast-in-python
        # https://gist.github.com/dksmiffs/96ddbfd11ad7349ab4889b2e79dc2b22
        pass

    @classmethod
    def get_alive_nodes(cls):
        def format_alive(node):
            return {
                'name': node[1]['name'],
                'location': node[0],
            }

        return list(
            map(
                format_alive,
                filter(
                    lambda nd: nd[1]['is_alive'],
                    cls.nodes.items(),
                )
            )
        )
