from fastapi import UploadFile
from kafka import KafkaProducer
from core.logger import get_logger
from core.event_handler import get_producer
from kafka.errors import InvalidTopicError, KafkaTimeoutError, KafkaConnectionError, KafkaUnavailableError
from kink import di
from .dto_operations import MakeBucketOperation, RemoveBucketOperation, UpdateOperation, RemoveOperation, UploadOperation
from .process_event import get_event

        
def producer_send(event:dict):
    producer:KafkaProducer = get_producer()
    try:
        producer.send(di['TOPIC'], event)
        get_logger('brainssys.databrain.publisher.process_publisher').info('Evento con info: ' + event['payload']['opp']['bucket'] + ' creado con exito')
    except InvalidTopicError as e:
        get_logger('brainssys.databrain.publisher.process_publisher').critical("Error del consumidor:" + str(e))
    except KafkaTimeoutError as e:
        get_logger('brainssys.databrain.publisher.process_publisher').critical("Error del consumidor:" + str(e))
    except KafkaConnectionError as e:
        get_logger('brainssys.databrain.publisher.process_publisher').critical("Error del consumidor:" + str(e))
    except KafkaUnavailableError as e:
        get_logger('brainssys.databrain.publisher.process_publisher').critical("Error del consumidor:" + str(e))


def proces_upload(opp: UploadOperation, file: UploadFile):
    if not opp.dict().get('object_name', []):
        opp = UploadOperation(bucket= opp.bucket,object_name= file.filename)
    event:dict = get_event(opp, file)
    producer_send(event)

def proces_update(opp: UpdateOperation, file: UploadFile):
    if not opp.dict().get('object_name', []):
        opp = UploadOperation(bucket= opp.bucket, object_name= file.filename)
    event:dict = get_event(opp, file)
    producer_send(event)

def proces_remove(opp: RemoveOperation):
    event:dict = get_event(opp)
    producer_send(event)

def proces_make_bucket(opp: MakeBucketOperation):
    event:dict = get_event(opp)
    producer_send(event)

def proces_remove_bucket(opp: RemoveBucketOperation):
    event:dict = get_event(opp)
    producer_send(event)




