from abc import ABC, abstractmethod
from typing import Protocol
from fastapi import UploadFile

class UploadOperation(Protocol):
    bucket:str
    object_name:str | None

class UpdateOperation(Protocol):
    bucket:str
    object_name:str | None

class RemoveOperation(Protocol):
    bucket:str
    object_name:str

class MakeBucketOperation(Protocol):
    bucket:str

class RemoveBucketOperation(Protocol):
    bucket:str


class IBusPublisher(ABC):
    
    @abstractmethod
    def _handle(self, obj: UpdateOperation | RemoveOperation | UploadOperation, payload:dict, id):
        ...

