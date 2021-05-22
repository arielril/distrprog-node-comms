from flask import request, current_app, abort


def validator():
    req_path = request._get_current_object().path

    accept_path = "supernode" if current_app.config["IS_SUPERNODE"] else "node"

    if accept_path in req_path.split("/"):
        current_app.logger.debug("--- good path ---")
    else:
        current_app.logger.debug("--- bad path ---")
        abort(418, description="I'm not your guy")
