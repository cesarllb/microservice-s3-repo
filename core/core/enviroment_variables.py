import os
from kink import di

def bootstrap():
    di['ENTITY_STORE'] = lambda _ : os.environ.get('MINIO_HTTP_HOST', 'localhost:9000')
    di['ENTITY_USER'] = lambda _ : os.environ.get('MINIO_HTTP_USER', 'minioadmin')
    di['ENTITY_PASSWORD'] = lambda _ : os.environ.get('MINIO_HTTP_PASSWORD', 'minioadmin')
    di['ENTITY_EXPIRE_TIME_HOURS'] = lambda _ : os.environ.get('ENTITY_EXPIRE_TIME_HOURS', '2')

    di['ELASTIC_HOST'] = lambda _ : os.environ.get('ELASTIC_HOST', "http://172.17.0.2:9200")
    di['ELASTIC_USER'] = lambda _ : os.environ.get('ELASTIC_USER', 'admin')
    di['ELASTIC_PASSWORD'] = lambda _ : os.environ.get('ELASTIC_PASSWORD', '<password>')
    di['ELASTIC_INDEX'] = lambda _ : os.environ.get('ELASTIC_INDEX', 'minio-test')

    di['EVENT_STORE'] = lambda _ : os.environ.get('EVENT_STORE', 'localhost:9092')
    di['TOPIC'] = lambda _ : os.environ.get('TOPIC', 'events')
    di['ENCODING'] = lambda _ : os.environ.get('ENCODING', 'utf-8')

    di['LOGGING_FORMAT'] = lambda _ : os.environ.get('LOGGING_FORMAT', '%(asctime)s %(levelname)-8s %(name)-12s %(message)s')
    di['LOGGING_ADRESS'] = lambda _ : os.environ.get('LOGGING_ADRESS', '/dev/log')