import time
from kafka import KafkaConsumer
from typing import Callable, Dict
from urllib.error import URLError
from core.logger import get_logger
from minio.error import MinioException
from core.event_handler import get_consumer
from .interfaces.bus_publisher import IBusPublisher
from kafka.errors import BrokerNotAvailableError, CommitFailedError, CorruptRecordException, RequestTimedOutError


class PublisherBuss(IBusPublisher):
    def __init__(self) -> None:
        self._handlers:Dict = dict()
        self._consumer_error = []
        
    def handler(self, type: str)->Callable:
        def decorator(function):
            if not type in self._handlers:
                self._handlers[type] = [function]
            else:
                self._handlers[type].append(function)
            return function
        return decorator
    
    def start_consumer(self) -> None:
        consumer:KafkaConsumer = get_consumer()
        get_logger('brainssys.databrain.core.handler').info("Conectado al TOPIC: " + str(consumer.subscription()))
        iterable = iter(consumer)
        total_time_passsed = 0
        multipler = 1
        while True:
            iter_time = time.time()
            try:
                event_record = next(iterable)
                self._handle(event_record.value.get('type'),
                            event_record.value.get('payload'),
                            event_record.value.get('id')
                            )
                get_logger('brainssys.databrain.core.handler').info("Evento del tipo: " + event_record.value.get('type') + 'con id: ' +  event_record.value.get('id') + ' consumido con éxito.')
            except BrokerNotAvailableError as e:
                get_logger('brainssys.databrain.handler').critical('Brocker no disponible. ' + str(e))
                self._consumer_error.append(event_record)
                continue
            except CommitFailedError as e:
                get_logger('brainssys.databrain.handler').critical('Fallo en hacer commit. ' + str(e))
                continue
            except CorruptRecordException as e:
                get_logger('brainssys.databrain.handler').critical('Record corrupto. ' + str(e))
                continue
            except RequestTimedOutError as e:
                get_logger('brainssys.databrain.handler').critical('Tiempo excedido. ' + str(e))
                self._consumer_error.append(event_record)
                continue
            except URLError as e:
                get_logger('brainssys.databrain.handler').critical('Error HTTP 403. ' + str(e))
                self._consumer_error.append(event_record)
                continue
            except MinioException as e:
                get_logger('brainssys.databrain.handler').critical('No existe el bucket especificado. ' + str(e))
                self._consumer_error.append(event_record)
                continue

            total_time_passsed += time.time() - iter_time
            if total_time_passsed > 40 * multipler:
                self.try_errors()
                multipler = multipler * 2

    def _handle(self, opp:str, payload:Dict, id) -> list:
        returns = []
        for handler_def in self._handlers[opp]:
            results= handler_def(payload, id)
            if results:
                returns.append(results)
        return returns

    def try_errors(self) -> None:
        try:
            for event_record in self._consumer_error:
                self._handle(event_record.value.get('type'),
                                event_record.value.get('payload'),
                                event_record.value.get('id')
                                )
                get_logger('brainssys.databrain.core.handler').info("Evento del tipo: " + event_record.value.get('type') + 'con id: ' +  event_record.value.get('id') + ' intentado por segunda vez y consumido con éxito.')
        except Exception:
            get_logger('brainssys.databrain.core.handler').critical('Error en el segundo intento de consumir este evento.')
    
