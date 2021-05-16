import os
from flask import Flask
from config import Config
from .api.errors import register_handlers as register_error_handlers


def setup_models(app):
    is_supernode = app.config['IS_SUPERNODE']

    print('##### ', app.config)
    if is_supernode:
        from .model import supernode
        snd = supernode.Supernode(
            app.config['MULTICAST_LOCATION'],
        )
    else:
        print('!@#3!312321@12#123!2331231#131231!#31312 ', app.config)
        filtered_resource = [
            p for p in app.config['RESOURCE_PATH'].split('/') if not p == '']
        node_resource_path = os.path.join(os.getcwd(), *filtered_resource)

        from .model import node
        nd = node.Node(
            app.config['SUPERNODE_ENDPOINT'],
        )
        nd.load_resources(node_resource_path)
        nd.register_to_supernode()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    setup_models(app)

    from .api.path_validator import validator
    app.before_request(validator)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    register_error_handlers(app)

    app.logger.info('api startup')

    return app
