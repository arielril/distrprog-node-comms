from flask import request, jsonify, abort

from ...api import bp
from ...api.util import format_response
from ...model.supernode import Supernode


@bp.route("/supernode/register", methods=["POST"])
def register():
    """
    {
        "name": "<node_name_opt>",
        "location": "<node_url>",
        "resources": [{
            "id": "<resource_id>",
            "name": "<resource_name>"
        }]
    }
    """

    req_data = request.get_json()

    if req_data == None:
        abort(400, description="No registration data was informed")
    elif not "location" in req_data:
        abort(400, description="node `location` is required")
    elif not "resources" in req_data:
        abort(400, description="node `resources` is required")

    (ok, error) = Supernode.register_node(
        req_data["location"],
        req_data["resources"],
        req_data["name"] if "name" in req_data else "",
    )

    if not ok and error == None:
        abort(500, description="Failed to register node")
    elif not ok and error != None:
        code = 500

        if isinstance(error, TypeError):
            code = 400

        abort(code, description=str(error))

    return "", 204


# GET /search/<file_id> | GET /search?node_name=<str>&file_name=<str>&hash_ids=<str>
@bp.route("/supernode/search/<string:file_id>", methods=["GET"])
def resource_search(file_id=""):
    # send the multicast search to other nodes
    data = {}

    if file_id != "":
        local_search = Supernode.get_resource_location_by_id(file_id)

        if "file" in local_search and "location" in local_search["file"]:
            data = local_search

    return format_response(
        data=data,
        entity="node_resource_location",
    )


@bp.route("/supernode/search", methods=["GET"])
def resource_list_search():
    hash_ids = request.args.get("hash_ids", "", type=str)
    hash_ids = [h.strip() for h in hash_ids.split(",") if len(h) > 0]

    resource_list = []

    for id in hash_ids:
        local_search = Supernode.get_resource_location_by_id(id)

        if "file" in local_search and "location" in local_search["file"]:
            resource_list.append(local_search)

    return format_response(
        data=resource_list,
        entity="node_resource_location",
    )


@bp.route("/supernode/alive", methods=["POST"])
def is_node_alive():
    # how to
    # https://stackoverflow.com/questions/21214270/how-to-schedule-a-function-to-run-every-hour-on-flask
    # https://blog.miguelgrinberg.com/post/run-your-flask-regularly-scheduled-jobs-with-cron
    # https://medium.com/thetiltblog/creating-scheduled-functions-in-python-apps-400ecea05bc3
    pass


@bp.route("/supernode/alive", methods=["GET"])
def get_alive_nodes():
    return format_response(
        data=Supernode.get_alive_nodes(),
        entity="node",
    )


@bp.route("/supernode/xxx", methods=["GET"])
def xxx():
    Supernode.check_alive_nodes()
    return "", 204
