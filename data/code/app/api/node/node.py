from flask import jsonify, abort

from ...api import bp
from ...model.node import Node


def get_resource_dict(id, name):
    return {
        'id': id,
        'name': name,
    }


def format_response(data={}, entity=''):
    p = {
        'data': data,
    }

    if not entity == '':
        p['entity'] = entity

    return jsonify(p)


@bp.route('/node/resources', methods=['GET'])
def list_resources():
    return format_response(
        data=list(map(
            lambda r: get_resource_dict(r[0], r[1]),
            Node.list_resources().items(),
        )),
        entity='resource',
    )


@bp.route('/node/resources/<id>', methods=['GET'])
def get_resource_info(id):
    resource_name = Node.get_resource(id)

    if resource_name == None:
        abort(404, description="Resource doesn't exist")

    return format_response(
        data=get_resource_dict(id, resource_name),
        entity='resource',
    )


@bp.route('/node/resources/<id>/download', methods=['GET'])
def download_resource():
    pass
