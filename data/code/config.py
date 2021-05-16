import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

env_file = 'supernode' if os.environ.get(
    'IS_SUPERNODE', '').strip() == 'true' else 'node'

load_dotenv(os.path.join(basedir, 'app', 'config', f'{env_file}.env'))


class Config(object):
    IS_SUPERNODE = os.environ.get('IS_SUPERNODE', '').strip() == 'true'
    SUPERNODE_ENDPOINT = os.environ.get('SUPERNODE_ENDPOINT', '').strip()
    RESOURCE_PATH = os.environ.get('RESOURCE_PATH', '').strip()
    MULTICAST_LOCATION = os.environ.get('MULTICAST_LOCATION', '').strip()
