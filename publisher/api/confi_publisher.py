import os
from kink import di


def boostrap():
    di['PUBLISHER_INTERFACE_HOST'] = lambda _ : os.environ.get('PUBLISHER_INTERFACE_HOST', 'localhost')
    di['PUBLISHER_INTERFACE_PORT'] = lambda _ : os.environ.get('PUBLISHER_INTERFACE_PORT', '8002')