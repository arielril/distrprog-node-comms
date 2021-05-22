import os
import logging

from flask import Flask
from config import Config
from .api.errors import register_handlers as register_error_handlers

# Logger configuration
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] "%(asctime)s" %(name)s : %(message)s',
)


def setup_models(app):
    is_supernode = app.config["IS_SUPERNODE"]
    loc = "{}:{}".format(
        app.config["LHOST"],
        app.config["LPORT"],
    )

    if is_supernode:
        from .model import supernode

        snd = supernode.Supernode(
            location=loc,
            multicast_loc=app.config["MULTICAST_LOCATION"],
            multicast_group_size=int(app.config["MULTICAST_GROUP_SIZE"], 10) - 1,
        )
    else:
        # LFI here
        filtered_resource = [p for p in app.config["RESOURCE_PATH"].split("/") if not p == ""]
        node_resource_path = os.path.join(os.getcwd(), *filtered_resource)

        from .model import node

        nd = node.Node(
            loc,
            app.config["SUPERNODE_ENDPOINT"],
        )
        nd.load_resources(node_resource_path)
        nd.register_to_supernode(app)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    setup_models(app)

    from .api.path_validator import validator

    app.before_request(validator)

    from app.api import bp as api_bp

    app.register_blueprint(api_bp, url_prefix="/api")

    register_error_handlers(app)

    app.logger.info("api startup")

    return app
