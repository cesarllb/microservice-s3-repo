import io
import os
import traceback
import uuid
import shutil
from kink import di
from pathlib import Path
from fastapi import UploadFile
from datetime import timedelta
from core.logger import get_logger
from tempfile import NamedTemporaryFile
from shutil import SpecialFileError, ReadError
from pydantic import BaseModel, NoneIsNotAllowedError
from core.object_storage import get_object_storage_client
from minio import InvalidResponseError, ServerError, S3Error
from .dto_operations import MakeBucketOperation, RemoveBucketOperation, RemoveOperation, UpdateOperation, UploadOperation


# def save_upload_file_tmp(upload_file: UploadFile) -> Path:
#     try:
#         suffix = Path(upload_file.filename).suffix
#         with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
#             shutil.copyfileobj(upload_file.file, tmp)
#             tmp_path = Path(tmp.name)
#     except SpecialFileError as e:
#         get_logger('brainssys.databrain.publisher').error("Error al copiar y/o obtener path del archivo en publisher.api.process_event.save_upload_file_tmp: " + str(e))
#     except ReadError as e:
#         get_logger('brainssys.databrain.publisher').error("Error al copiar y/o obtener path del archivo en publisher.api.process_event.save_upload_file_tmp: " + str(e))
#     finally:
#         upload_file.file.close()
#     return tmp_path

# def remove_temp_file(path:str):
#     try:
#         os.remove(path)
#     except OSError as error:
#         get_logger('brainssys.databrain.publisher').error("Error al eliminar archivo en publisher.api.process_event.remove_temp_file: " + error )

#Guarda el archivo en un bucket temporal de MinIO y devuelve su url para ser enviada hacia Kafka
def put_temp_object(file:UploadFile, obj_name:str):
    try:
        # path = save_upload_file_tmp(file)

        client = get_object_storage_client()

        if not client.bucket_exists(bucket_name='temp'):
            client.make_bucket(bucket_name='temp')

        file_size = os.fstat(file.file.fileno()).st_size
        client.put_object(bucket_name='temp', object_name=obj_name, data=file.file, length= file_size)
        
        return client.presigned_get_object(bucket_name='temp', object_name=obj_name, expires=timedelta(hours=int(di['ENTITY_EXPIRE_TIME_HOURS'])))

    except InvalidResponseError as e:
        get_logger('brainssys.databrain.publisher').error("Error en MinIO en publisher.api.process_event.get_temp_url: " + str(e))
    except ServerError as e:
        get_logger('brainssys.databrain.publisher').error("Error en MinIO en publisher.api.process_event.get_temp_url: " + str(e))
    except S3Error as e:
        get_logger('brainssys.databrain.publisher').error("Error en S3Error en publisher.api.process_event.get_temp_url: " + str(e))

def get_operation(opp) -> str:
    otype = opp.__class__.__name__
    operations_dict:dict[str, str] = {
                        UploadOperation.__name__: 'UploadOperation',
                        UpdateOperation.__name__: 'UpdateOperation',
                        RemoveOperation.__name__: 'RemoveOperation',
                        MakeBucketOperation.__name__: 'MakeBucketOperation',
                        RemoveBucketOperation.__name__: 'RemoveBucketOperation',    
                    }
    return operations_dict.get(otype, [])

class Event(BaseModel):
    type:str
    id:str
    version:str
    payload:dict

def get_event(opp: UploadOperation | UpdateOperation | RemoveOperation | MakeBucketOperation | RemoveBucketOperation, file: UploadFile = None) -> dict:
    id = str(uuid.uuid1().int)
    operation = get_operation(opp)
    if operation:
        event:dict = Event(type='brainssys.datebrain.publisher.' + str(operation), 
                            id=id,
                            version = '1.0',
                            payload = {'opp': {'bucket': opp.bucket}}
                            ).dict()
    else:
        raise NoneIsNotAllowedError()

    if isinstance(opp, UploadOperation) or isinstance(opp, UpdateOperation) or isinstance(opp, RemoveOperation):
        event['payload']['opp']['object_name'] = opp.object_name
        if not isinstance(opp, RemoveOperation):
            put_temp_object(file, opp.object_name)


    return event
