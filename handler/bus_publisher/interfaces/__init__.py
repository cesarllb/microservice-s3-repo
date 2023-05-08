from fastapi import UploadFile
from .operations import IRemover, IUpdater, IUploader, IMakeBucket, IRemoveBucket


class Repo(IUploader, IUpdater, IRemover, IMakeBucket, IRemoveBucket):
    def __init__(self, uploader:IUploader, updater:IUpdater, remover:IRemover, maker_bucket: IMakeBucket, remover_bucket: IRemoveBucket) -> None:
        self._uploader = uploader
        self._updater = updater
        self._remover = remover
        self._maker_bucket = maker_bucket
        self._remover_bucket = remover_bucket
        
    
    def upload(self, bucket:str ,  object_name:str, file:UploadFile):
        return self._uploader.upload_obj(bucket, object_name, file)
    
    def update(self, bucket:str ,  object_name:str , file: UploadFile):
        return self._updater.update_obj(bucket, object_name, file)

    def remove(self, bucket:str, object_name:str):
        return self._remover.remove_obj(bucket, object_name)

    def make_bucket(self, bucket:str):
        return self._maker_bucket.make_bucket(bucket)

    def remove_bucket(self, bucket:str):
        return self._remover_bucket.remove_bucket(bucket)