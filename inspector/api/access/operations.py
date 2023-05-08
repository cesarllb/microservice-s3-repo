from kink import di
from minio import Minio
from datetime import timedelta
from core.logger import get_logger
from core.search_engine import search_document
from core.object_storage import get_object_storage_client
from minio.error import InvalidResponseError, S3Error, MinioException
from .interfaces.repository_inspector.operations import IGeter, IListBuckets, IListObjects
from elasticsearch.exceptions import BadRequestError, ConnectionTimeout, TransportError, ApiError


repo = {}
client = get_object_storage_client()

class Get(IGeter):

    def __init__(self):
        super().__init__()
        self.client:Minio =  client

    def get(self, bucket:str, object_name:str):
        if self.client.bucket_exists(bucket):
            try:
                url = self.client.presigned_get_object(bucket, object_name, expires=timedelta(hours=int(di['ENTITY_EXPIRE_TIME_HOURS'])))
                get_logger('brainssys.databrain.core.inspector').info("Mostrando objeto del bucket " + bucket)
                return url
            except InvalidResponseError as e:
                get_logger('brainssys.databrain.core.inspector').error("Respuesta invalida: " + str(e))
            except S3Error as e:
                get_logger('brainssys.databrain.core.inspector').error("Error S3: " + str(e))
            except MinioException as e:
                get_logger('brainssys.databrain.core.inspector').error("Excepcion de MinIO: " + str(e))    

        
class ListObjects(IListObjects):

    def __init__(self):
        super().__init__()
        self.client:Minio = client

    def list_objects(self, bucket:str = "", object_name:str = "") -> list:
        try:
            resp = search_document(index=di['ELASTIC_INDEX'], document={
                                        'bucket': bucket, 
                                        'object_name': object_name
                                    })
            all_hits = resp['hits']['hits']
            data = []
            if resp:
                for _, doc in enumerate(all_hits):
                    data.append(doc)

            else:
                get_logger('brainssys.databrain.core.inspector').info("No se encontraron elementos")
            return data
        except BadRequestError as e:
            get_logger('brainssys.databrain.core.inspector').error("Petición inválida: " + str(e))
        except ConnectionTimeout as e:
            get_logger('brainssys.databrain.core.inspector').error("Tiempo para la conexión excedido: " + str(e))
        except TransportError as e:
            get_logger('brainssys.databrain.core.inspector').error("Error en la transportación: " + str(e))
        except ApiError as e:
            get_logger('brainssys.databrain.core.inspector').error("Error en la API: " + str(e))

class ListBuckets(IListBuckets):

    def __init__(self):
        super().__init__()
        self.client:Minio = client
        
    def list_all_buckets(self) -> list:
        try:
            buckets = client.list_buckets()
            list_names = []
            for b in buckets:
                list_names.append(b.name + ' : ' + str(b.creation_date))
            get_logger('brainssys.databrain.core.inspector').info("Mostrando todos los buckets")
            return list_names
        except InvalidResponseError as e:
            get_logger('brainssys.databrain.core.inspector').error("Respuesta invalida: " + str(e))
        except S3Error as e:
            get_logger('brainssys.databrain.core.inspector').error("Error S3: " + str(e))
        except MinioException as e:
            get_logger('brainssys.databrain.core.inspector').error("Excepcion de MinIO: " + str(e))
