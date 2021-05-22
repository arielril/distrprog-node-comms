from flask import jsonify, abort, request

from ...api import bp
from ...api.util import format_response
from ...model.node import Node


def get_resource_dict(id, name):
    return {
        "id": id,
        "name": name,
    }


@bp.route("/node/resources", methods=["GET"])
def list_resources():
    return format_response(
        data=list(
            map(
                lambda r: get_resource_dict(r[0], r[1]),
                Node.list_resources().items(),
            )
        ),
        entity="resource",
    )


@bp.route("/node/resources/<string:id>", methods=["GET"])
def get_resource_info(id):
    resource_info = Node.get_resource(id)

    if resource_info == None:
        supernode_resource = Node.supernode_search_resource(id)

        if supernode_resource == None:
            abort(404, description="Resource doesn't exist")

        resource_info = supernode_resource

    if isinstance(resource_info, str):
        return format_response(
            data=get_resource_dict(id, resource_info),
            entity="resource",
        )
    elif isinstance(resource_info, dict):
        return (
            format_response(
                data={
                    "id": id,
                    "info": resource_info,
                },
                entity="resource",
            ),
            302,
        )


# /node/resources/find?hash_ids=13123132,12312
@bp.route("/node/resources/find", methods=["GET"])
def find_resources():
    hash_ids = request.args.get("hash_ids", "", type=str)
    hash_ids = [h.strip() for h in hash_ids.split(",") if len(h) > 0]

    resource_list = []

    for id in hash_ids:
        resource_info = Node.get_resource(id)

        if resource_info == None:
            supernode_resource = Node.supernode_search_resource(id)

            if supernode_resource == None:
                continue

            resource_info = supernode_resource

        if isinstance(resource_info, str):
            resource_list.append(get_resource_dict(id, resource_info))
        elif isinstance(resource_info, dict):
            resource_list.append(
                {
                    "id": id,
                    "info": resource_info,
                }
            )

    return format_response(
        data=resource_list,
        entity="resource",
    )


@bp.route("/node/health", methods=["GET"])
def health():
    return "", 200
