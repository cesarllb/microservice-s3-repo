from kink import inject
from .bus import InspectorBus
from .interfaces.bus_inspector import IBusInspector
from .interfaces.bus_inspector import GetOperation, ListObjectsOperation
from .interfaces.repository_inspector.operations import IGeter, IListBuckets, IListObjects

def buss()->IBusInspector:
    buss = InspectorBus()
    
    @buss.handler('GetOperation')
    @inject
    def get(opp:GetOperation, repo:IGeter):
        return repo.get(opp.bucket, opp.object_name)

    @buss.handler('ListBucketsOperation')
    @inject
    def list_all_buckets(repo:IListBuckets):
        return repo.list_all_buckets()

    @buss.handler('ListObjectsOperation')
    @inject
    def list_objects(opp:ListObjectsOperation, repo:IListObjects):
        return repo.list_objects(opp.bucket, opp.object_name)

    return buss