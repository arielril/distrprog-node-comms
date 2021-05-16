import os
from flask import Flask
from config import Config


def setup_models(app):
    is_supernode = app.config['IS_SUPERNODE']

    if is_supernode:
        # from .model import supernode
        # snd = supernode.Supernode()
        pass
    else:
        filtered_resource = [
            p for p in app.config['RESOURCE_PATH'].split('/') if not p == '']
        node_resource_path = os.path.join(os.getcwd(), *filtered_resource)

        from .model import node
        nd = node.Node(
            node_resource_path,
            app.config['SUPERNODE_ENDPOINT'],
        )


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    setup_models(app)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    app.logger.info('api startup')

    return app
