from datetime import datetime
from flask import current_app
import requests
import threading
from uuid import uuid4

from .udp import Multi


class Supernode:
    # entry => ['<file_hash>'] -> { file_name:str, node_location }
    node_resources = {}

    # entry => ['<node_location>'] -> { is_alive:bool, last_check:time }
    nodes = {}

    multicast_location = ""
    location = ""
    multicast_group_size = []
    name = str(uuid4())

    def __init__(self, location="", multicast_loc="", multicast_group_size=0):
        super().__init__()
        self.multicast_location = multicast_loc
        self.location = location
        self.multicast_group_size.append(multicast_group_size)

        self.multi = Multi(self, self.multicast_group_size, supernode_name=self.name)
        t = threading.Thread(target=self.multi.receive)
        t.start()

        # from ..background.supernode_alive import start_task

        # start_task(location)

    @classmethod
    def register_node(cls, location: str, resource_list, name="") -> (bool, Exception):
        if not isinstance(resource_list, list):
            return False, TypeError("node `resources` must be a list")

        if len(resource_list) == 0:
            # ignore nodes without resources, just gabage
            return True, None

        cls.nodes[location] = {
            "is_alive": True,
            "last_check": datetime.now(),
            "name": name,
        }

        for r in resource_list:
            cls.node_resources[r["id"]] = {
                "file_name": r["name"],
                "node_location": location,
            }

        return True, None

    @classmethod
    def get_resource_location_by_id(cls, id: str):
        """
        # file doesn't exists here, need to search with the other supernodes
        return format
            [{
                "id": "<file_id>",
                "file": {
                    "name": "<file_name>",
                    "location": "<file_location>"
                }
            }]
        """
        response = {
            "id": id,
            "file": {},
        }

        current_app.logger.debug(f"node resources ({cls.node_resources})")
        if id in cls.node_resources:
            current_app.logger.debug(f"found resource ({id}) locally")

            file_info = cls.node_resources[id]
            response["file"] = {
                "name": file_info["file_name"],
                "location": file_info["node_location"],
            }
        else:
            current_app.logger.info(f"searching resource ({id}) in other supernodes")

            multi = Multi(cls, msgs_num=cls.multicast_group_size[0], supernode_name=cls.name)
            file_location = multi.request_file_search_and_listen(id)
            print("#@@@!!! received file location", file_location)

            if file_location != None:
                response["file"]["location"] = file_location

        return response

    @classmethod
    def multicasting(cls, file_id=""):
        # https://pymotw.com/2/socket/multicast.html
        # https://stackoverflow.com/questions/603852/how-do-you-udp-multicast-in-python
        # https://gist.github.com/dksmiffs/96ddbfd11ad7349ab4889b2e79dc2b22
        if file_id == "":
            return None

        search_result = cls.multi.request_file_search_and_listen(file_id)

        if search_result == None:
            return None

        response = {
            "id": file_id,
            "file": {
                "location": search_result,
            },
        }
        return response

    @classmethod
    def get_alive_nodes(cls):
        def format_alive(node):
            return {
                "name": node[1]["name"],
                "location": node[0],
            }

        return list(
            map(
                format_alive,
                filter(
                    lambda nd: nd[1]["is_alive"],
                    cls.nodes.items(),
                ),
            )
        )

    @classmethod
    def _remove_resources_from_node(cls, location=""):
        filtered_node_resources = {}
        for (fhash, d) in cls.node_resources.items():
            if "node_location" in d and d["node_location"] != location:
                filtered_node_resources[fhash] = d

        cls.node_resources = filtered_node_resources

    @classmethod
    def _check_and_remove_dead_node(cls, location=""):
        alive_time_diff = datetime.now() - cls.nodes[location]["last_check"]
        if alive_time_diff.total_seconds() > 10:
            current_app.logger.debug(f"[+] node ({location}) is dead!")
            cls._remove_resources_from_node(location)
            current_app.logger.warn(f"[+] node ({location}) removed!")
            # dead
            return True
        # alive
        return False

    @classmethod
    def _remove_nodes(cls, node_lst=[]):
        for location in node_lst:
            cls.nodes.pop(location, None)

    @classmethod
    def check_alive_nodes(cls):
        remove_nodes = []
        for (k, v) in cls.nodes.items():
            if cls._check_and_remove_dead_node(k):
                # node is dead
                remove_nodes.append(k)

            try:
                res = requests.get(
                    f"http://{k}/api/node/health",
                    timeout=2,
                )

                if res.status_code == 200:
                    current_app.logger.debug(f"[+] node ({k}) is alive")
                    cls.nodes[k]["is_alive"] = True
                    cls.nodes[k]["last_check"] = datetime.now()
                else:
                    current_app.logger.warn(f"[+] node ({k}) didn't answered for liveness")

            except Exception:
                current_app.logger.error(f"[.] failed to get node aliveness")
        cls._remove_nodes(remove_nodes)
