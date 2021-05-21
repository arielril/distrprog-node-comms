from flask import request, jsonify, abort

from ...api import bp
from ...api.util import format_response
from ...model.supernode import Supernode


@bp.route('/supernode/register', methods=['POST'])
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
        abort(400, description='No registration data was informed')
    elif not 'location' in req_data:
        abort(400, description='node `location` is required')
    elif not 'resources' in req_data:
        abort(400, description='node `resources` is required')

    (ok, error) = Supernode.register_node(
        req_data['location'],
        req_data['resources'],
        req_data['name'] if 'name' in req_data else '',
    )

    if not ok and error == None:
        abort(500, description='Failed to register node')
    elif not ok and error != None:
        code = 500

        if isinstance(error, TypeError):
            code = 400

        abort(code, description=str(error))

    return '', 204


# TODO GET /search/<file_id> | GET /search?node_name=<str>&file_name=<str>&hash_id=<str>
@bp.route('/supernode/search', methods=['GET'])
@bp.route('/supernode/search/<string:file_id>', methods=['GET'])
def resource_search(file_id=''):
    # send the multicast search to other nodes
    data = {}

    if file_id != '':
        data = Supernode.get_resource_location_by_id(file_id)

    return format_response(
        data=data,
        entity='node_resource_location',
    )


@bp.route('/supernode/alive', methods=['POST'])
def is_node_alive():
    # how to
    # https://stackoverflow.com/questions/21214270/how-to-schedule-a-function-to-run-every-hour-on-flask
    # https://blog.miguelgrinberg.com/post/run-your-flask-regularly-scheduled-jobs-with-cron
    # https://medium.com/thetiltblog/creating-scheduled-functions-in-python-apps-400ecea05bc3
    pass


@bp.route('/supernode/alive', methods=['GET'])
def get_alive_nodes():
    return format_response(
        data=Supernode.get_alive_nodes(),
        entity='node',
    )


@bp.route('/supernode/xxx', methods=['GET'])
def xxx():
    Supernode.check_alive_nodes()
    return '', 204
