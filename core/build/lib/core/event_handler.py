from json import dumps, loads
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaTimeoutError, KafkaError
import core.enviroment_variables
from core.logger import get_logger
from kink import di


def get_consumer() -> None:
        try:
            consumer = KafkaConsumer(di['TOPIC'],
                                          bootstrap_servers=[di['EVENT_STORE']],
                                          auto_offset_reset='earliest',
                                          enable_auto_commit=True,
                                          group_id='event_group',
                                          value_deserializer=lambda x: loads(x.decode(di['ENCODING'])))
            get_logger('brainssys.databrain.core.event_handler').info('Consumer conectado a Event Store')
            return consumer
        except KafkaTimeoutError as e:
            get_logger('brainssys.databrain.core.event_handler').critical("Error de Kafka Consumer: tiempo de espera excedido", str(e))
        except KafkaError as e:
            get_logger('brainssys.databrain.core.event_handler').critical('Error interno de Kakfa', str(e))
            

def get_producer() -> KafkaProducer:
    try:
        return KafkaProducer(bootstrap_servers=[di['EVENT_STORE']],
                        value_serializer=lambda x: dumps(x).encode(di['ENCODING']))
    except KafkaTimeoutError as e:
        get_logger('brainssys.databrain.core.event_handler').critical("Error de Kafka Consumer: tiempo de espera excedido", str(e))
    except KafkaError as e:
        get_logger('brainssys.databrain.core.event_handler').critical('Error interno de Kakfa', str(e))