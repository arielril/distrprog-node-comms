import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

env_file = 'supernode' if os.environ.get('IS_SUPERNODE') == 'true' else 'node'

load_dotenv(os.path.join(basedir, 'app', 'config', f'{env_file}.env'))


class Config(object):
    IS_SUPERNODE = os.environ.get('IS_SUPERNODE') == 'true'
    SUPERNODE_ENDPOINT = os.environ.get('SUPERNODE_ENDPOINT')
    RESOURCE_PATH = os.environ.get('RESOURCE_PATH')
