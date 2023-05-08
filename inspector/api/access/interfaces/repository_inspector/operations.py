# Implementamos interface
from abc import ABC, abstractmethod

class IGeter( ABC ):

    @abstractmethod
    def get(self, bucket:str, object_name:str):
        ...

class IListBuckets( ABC ):

    @abstractmethod
    def list_all_buckets(self):
        ...

class IListObjects( ABC ):

    @abstractmethod
    def list_objects(self, bucket:str, object_name:str):
        ...

        