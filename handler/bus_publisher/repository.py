import os
from kink import di
from minio import Minio
from urllib3 import HTTPResponse
from core.logger import get_logger
from elasticsearch import Elasticsearch
from core.search_engine import get_search_engine
from core.object_storage import get_object_storage_client
from minio.error import InvalidResponseError, S3Error, MinioException
from core.search_engine import delete_document, index_document, update_document
from .interfaces.operations import IMakeBucket, IRemoveBucket, IRemover, IUploader, IUpdater


repo = {}
client = get_object_storage_client()
search = get_search_engine()

class Upload(IUploader):

    def __init__(self):
        super().__init__()
        self.client:Minio = client
        self.search:Elasticsearch = search

    def upload_obj(self, bucket:str, id, object_name:str):
        if self.client.bucket_exists(bucket):
            try:
                with self.client.get_object(bucket_name='temp', object_name=object_name) as response:
                    file_size = int(response.getheader('Content-Length'))
                    data_file = self.client.put_object(bucket_name=bucket, object_name=object_name, data=response, length= file_size)
                #Delete temporal object created in MinIO
                self.client.remove_object(bucket_name='temp', object_name=object_name)
                self.client.remove_bucket(bucket_name='temp')
                get_logger('brainssys.databrain.core.handler').info(f'Objeto "{object_name}" creado en el bucket "{bucket}"')
                try:
                    index_document(di['ELASTIC_INDEX'], {
                                        'bucket': bucket,
                                        'object_name': object_name,
                                        'id': id
                                    }, id)
                except:
                    get_logger('brainssys.databrain.core.handler').critical("Upload no pudo conectarse a elastik")
                return data_file
            except InvalidResponseError as e:
                get_logger('brainssys.databrain.core.inspector').error("Respuesta invalida: " + str(e))
            except S3Error as e:
                get_logger('brainssys.databrain.core.inspector').error("Error S3: " + str(e))
            except MinioException as e:
                get_logger('brainssys.databrain.core.inspector').error("Excepcion de MinIO: " + str(e))

                
        else:
            get_logger('brainssys.databrain.core.handler').critical("No existe el bucket especificado")
            raise MinioException("No existe el bucket especificado")



class Update(IUpdater):

    def __init__(self):
        super().__init__()
        self.client:Minio = client
        self.search:Elasticsearch = search

    def update_obj(self, bucket:str, id, object_name:str):
        if self.client.bucket_exists(bucket):
            try:
                self.client.remove_object(bucket, object_name)
            except InvalidResponseError as e:
                get_logger('brainssys.databrain.core.inspector').error("Respuesta invalida: " + str(e))
            except S3Error as e:
                get_logger('brainssys.databrain.core.inspector').error("Error S3: " + str(e))
            except MinioException as e:
                get_logger('brainssys.databrain.core.inspector').error("Excepcion de MinIO: " + str(e))
            try:
                with self.client.get_object(bucket_name='temp', object_name=object_name) as response:
                    file_size = int(response.getheader('Content-Length'))
                    data_file = self.client.put_object(bucket_name=bucket, object_name=object_name, data=response, length= file_size)
                #Delete temporal object created in MinIO
                self.client.remove_object(bucket_name='temp', object_name=object_name)
                self.client.remove_bucket(bucket_name='temp')

                get_logger('brainssys.databrain.core.handler').info(f'Objeto "{object_name}" actualizado en el bucket "{bucket}"')
                #elastic update
                try:
                    update_document(di['ELASTIC_INDEX'], {
                                        'bucket': bucket,
                                        'object_name': object_name
                                    }, id)
                except:
                    get_logger('brainssys.databrain.core.handler').critical("Update no pudo conectarse a elastik")
                return data_file
            except InvalidResponseError as e:
                get_logger('brainssys.databrain.core.inspector').error("Respuesta invalida: " + str(e))
            except S3Error as e:
                get_logger('brainssys.databrain.core.inspector').error("Error S3: " + str(e))
            except MinioException as e:
                get_logger('brainssys.databrain.core.inspector').error("Excepcion de MinIO: " + str(e))

        get_logger('brainssys.databrain.core.handler').critical("No existe el bucket especificado")
        raise MinioException("No existe el bucket especificado")
            
        

class Remove(IRemover):

    def __init__(self):
        super().__init__()
        self.client:Minio = client
        self.search:Elasticsearch = search


    def remove_obj(self, bucket:str, id, object_name:str):
        if self.client.bucket_exists(bucket):
            try:
                self.client.remove_object(bucket, object_name)
                get_logger('brainssys.databrain.core.handler').info(f'Objeto "{object_name}" eliminado en el bucket "{bucket}"')
                try:
                    #elastic delete
                    delete_document(di['ELASTIC_INDEX'], id)
                except:
                    get_logger('brainssys.databrain.core.handler').critical("Update no pudo conectarse a elastik")
            except InvalidResponseError as e:
                get_logger('brainssys.databrain.core.inspector').error("Respuesta invalida: " + str(e))
            except S3Error as e:
                get_logger('brainssys.databrain.core.inspector').error("Error S3: " + str(e))
            except MinioException as e:
                get_logger('brainssys.databrain.core.inspector').error("Excepcion de MinIO: " + str(e))
        else:
            get_logger('brainssys.databrain.core.handler').critical("No existe el bucket especificado")
            raise MinioException("No existe el bucket especificado")


class MakeBucket(IMakeBucket):

    def __init__(self):
        super().__init__()
        self.client:Minio = client

    def make_bucket(self, bucket:str):
        if not self.client.bucket_exists(bucket):
            try:
                self.client.make_bucket(bucket)
                get_logger('brainssys.databrain.core.handler').info(f'Bucket {bucket} creado con exito')
            except InvalidResponseError as e:
                get_logger('brainssys.databrain.core.inspector').error("Respuesta invalida: " + str(e))
            except S3Error as e:
                get_logger('brainssys.databrain.core.inspector').error("Error S3: " + str(e))
            except MinioException as e:
                get_logger('brainssys.databrain.core.inspector').error("Excepcion de MinIO: " + str(e))
        else:
            get_logger('brainssys.databrain.core.handler').critical("Ya existe el bucket especificado")
            raise MinioException("Ya existe el bucket especificado")

class RemoveBucket(IRemoveBucket):

    def __init__(self):
        super().__init__()
        self.client:Minio = client

    def remove_bucket(self, bucket:str):
        if self.client.bucket_exists(bucket):
            try:
                self.client.remove_bucket(bucket)
                get_logger('brainssys.databrain.core.handler').info(f'Bucket {bucket} eliminado con exito')
            except InvalidResponseError as e:
                get_logger('brainssys.databrain.core.inspector').error("Respuesta invalida: " + str(e))
            except S3Error as e:
                get_logger('brainssys.databrain.core.inspector').error("Error S3: " + str(e))
            except MinioException as e:
                get_logger('brainssys.databrain.core.inspector').error("Excepcion de MinIO: " + str(e))
        else:       
            get_logger('brainssys.databrain.core.handler').critical("No existe el bucket especificado")
            raise MinioException("No existe el bucket especificado")

