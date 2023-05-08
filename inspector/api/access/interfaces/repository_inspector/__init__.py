from typing import Optional
from .operations import IGeter, IListBuckets, IListObjects


class Repo(IGeter, IListBuckets, IListObjects):
    def __init__(self, geter:IGeter, list_objects:IListObjects, list_buckets:IListBuckets) -> None:
        self._geter = geter
        self._list_objects = list_objects
        self._list_buckets = list_buckets
    
    def get(self, bucket:str, object_name:str):
        return self._geter.get(bucket, object_name)
    
    def list_buckets(self):
        return self._list_buckets.list_buckets()

    def list_objects(self, bucket:str, prefix: Optional[str] = None):
        return self._list_objects.list_objects(bucket, prefix)