import os
from kink import di
from .access.builder import buss
from .access.interfaces.bus_inspector import IBusInspector
from .access.operations import ListBuckets, ListObjects, Get
from .access.interfaces.repository_inspector.operations import IGeter, IListBuckets, IListObjects

def config():
    boostrap()
    di[IBusInspector] = buss()
    di[IGeter] = Get()
    di[IListBuckets] = ListBuckets()
    di[IListObjects] = ListObjects()

def boostrap():
    di['INSPECTOR_INTERFACE_HOST'] = lambda _ : os.environ.get('INSPECTOR_INTERFACE_HOST', 'localhost')
    di['INSPECTOR_INTERFACE_PORT'] = lambda _ : os.environ.get('INSPECTOR_INTERFACE_PORT', '8001')