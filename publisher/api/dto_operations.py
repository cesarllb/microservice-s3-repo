from pydantic import BaseModel


class UploadOperation(BaseModel):
    bucket:str
    object_name:str | None

class UpdateOperation(BaseModel):
    bucket:str
    object_name:str | None

class RemoveOperation(BaseModel):
    bucket:str
    object_name:str

class MakeBucketOperation(BaseModel):
    bucket:str

class RemoveBucketOperation(BaseModel):
    bucket:str



