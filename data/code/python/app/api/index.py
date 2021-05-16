from . import bp


@bp.route('/', methods=['GET'])
def idx():
    return 'index guy!'
