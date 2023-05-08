from fastapi import UploadFile
from abc import ABC, abstractmethod


class IUploader( ABC ):

    @abstractmethod
    def upload_obj(self, bucket:str , id, object_name:str = None):
        ...

class IUpdater( ABC ):

    @abstractmethod
    def update_obj(self, bucket:str ,  id, object_name:str = None):
        ...

class IRemover( ABC ):

    @abstractmethod
    def remove_obj(self, bucket:str, id, object_name:str):
        ...

class IMakeBucket( ABC ):

    @abstractmethod
    def make_bucket(self, bucket:str):
        ...

class IRemoveBucket( ABC ):

    @abstractmethod
    def remove_bucket(self, bucket:str):
        ...



        