from flask import jsonify

from ...api import bp
from ...model.node import Node


@bp.route('/node/resources', methods=['GET'])
def list_resources():
    return jsonify(list(map(
        lambda r: dict({
            'id': r[0],
            'name': r[1],
        }),
        Node.list_resources().items(),
    )))


@bp.route('/node/resources/<id>', methods=['GET'])
def get_resource_info(id):
    return {'name': Node.get_resource(id)}


@bp.route('/node/resources/<id>/download', methods=['GET'])
def download_resource():
    pass
