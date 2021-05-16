from app.api import bp


@bp.route('/supernode/register', methods=['POST'])
def register():
    pass


# TODO GET /search/<hash_id> | GET /search?q=<search_str>
@bp.route('/supernode/search', methods=['GET'])
def resource_search():
    # send the multicast search to other nodes
    pass


@bp.route('/supernode/alive', methods=['POST'])
def is_node_alive():
    # how to
    # https://stackoverflow.com/questions/21214270/how-to-schedule-a-function-to-run-every-hour-on-flask
    # https://blog.miguelgrinberg.com/post/run-your-flask-regularly-scheduled-jobs-with-cron
    # https://medium.com/thetiltblog/creating-scheduled-functions-in-python-apps-400ecea05bc3
    pass
