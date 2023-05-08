from fastapi import APIRouter, Depends, File, UploadFile
from .process_publisher import proces_make_bucket, proces_remove_bucket, proces_update, proces_upload, proces_remove
from .dto_operations import UpdateOperation, RemoveOperation, UploadOperation, MakeBucketOperation, RemoveBucketOperation

repo = APIRouter()

@repo.post('/upload/')
async def upload(opp: UploadOperation = Depends(), file: UploadFile = File(...)) -> str:
    proces_upload(opp, file)
    return {"operation": "brainssys.databrain.publisher.upload", "bucket": opp.bucket}

@repo.post('/update/')
async def update(opp: UpdateOperation = Depends(), file: UploadFile = File(...)) -> str:
    proces_update(opp, file)
    return {"operation": "brainssys.databrain.publisher.update", "bucket": opp.bucket}

@repo.delete('/remove/')
async def remove(opp: RemoveOperation = Depends()) -> str:
    proces_remove(opp)
    return {"operation": "brainssys.databrain.publisher.remove", "bucket": opp.bucket, "object_name": opp.object_name}

@repo.post('/bucket/')
async def make_bucket(opp: MakeBucketOperation = Depends()) -> str:
    proces_make_bucket(opp)
    return {"operation": "brainssys.databrain.publisher.make_bucket", "bucket": opp.bucket}

@repo.delete('/bucket/')
async def remove_bucket(opp: RemoveBucketOperation = Depends()) -> str:
    proces_remove_bucket(opp)
    return {"operation": "brainssys.databrain.publisher.remove_bucket", "bucket": opp.bucket}

