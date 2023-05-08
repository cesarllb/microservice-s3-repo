from kink import di
from fastapi import APIRouter, Depends
from pyparsing import Optional
from .access.interfaces.bus_inspector import IBusInspector
from .access.interfaces.bus_inspector import GetOperation, ListObjectsOperation

def buss() -> IBusInspector:
    return di[IBusInspector]

repo = APIRouter()

@repo.get('/get_object/')
async def get_object(bucket: str, object_name: str, b: IBusInspector = Depends(buss)):
    opp = GetOperation(bucket = bucket, object_name=object_name)
    return {
        'data': b.handle(opp)
    }

@repo.get('/list_objects/')
async def list_objects(bucket: str, object_name: str | None = None, b: IBusInspector = Depends(buss)):
    opp = ListObjectsOperation(bucket = bucket, object_name = object_name)
    return {
        'data': b.handle(opp)
    }

@repo.get('/list_buckets/')
async def list_buckets(b: IBusInspector = Depends(buss)):
    return {
        'data': b.handle()
    }