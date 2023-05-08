from abc import ABC, abstractmethod
from pydantic import BaseModel


class GetOperation(BaseModel):
    bucket:str
    object_name:str

class ListObjectsOperation(BaseModel):
    bucket:str
    object_name:str | None


class IBusInspector(ABC):
    
    @abstractmethod
    def handle(self, obj: GetOperation | ListObjectsOperation = None):
        ...