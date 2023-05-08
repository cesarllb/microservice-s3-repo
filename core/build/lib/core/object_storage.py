from kink import di
from minio import Minio
from minio.error import MinioException, ServerError, S3Error
from minio.error import S3Error
from core.logger import get_logger


def get_object_storage_client()->Minio:
    try:
        client:Minio = Minio(
            di['ENTITY_STORE'],
            di['ENTITY_USER'],
            di['ENTITY_PASSWORD'],
            secure=False,
        )
        get_logger('brainssys.databrain.core.object_storage').info('Cliente conectado a Entity Store')
        return client
    except S3Error as e:
        get_logger('brainssys.databrain.core.object_storage').critical('Fallo en la conexion a brainssys.databrain.core.get_object_storage_client:', str(e))
    except MinioException as e:
        get_logger('brainssys.databrain.core.object_storage').critical('Fallo en la conexion a brainssys.databrain.core.get_object_storage_client:', str(e))
