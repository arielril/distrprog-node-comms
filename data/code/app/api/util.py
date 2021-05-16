from flask import jsonify


def format_response(data={}, entity=''):
    p = {
        'data': data,
    }

    if not entity == '':
        p['entity'] = entity

    return jsonify(p)
