from elastic_transport import ObjectApiResponse
from elasticsearch import Elasticsearch
from kink import di
from elasticsearch.exceptions import ConnectionError, ConnectionTimeout, BadRequestError, NotFoundError, TransportError
import core.enviroment_variables
from core.logger import get_logger


def get_search_engine() -> Elasticsearch:
    try:
        es = Elasticsearch(di['ELASTIC_HOST'])
        get_logger('brainssys.databrain.core.search_engine').info('Cliente conectado a ElasticSearch')
        return es
    except ConnectionError as e:
        get_logger('brainssys.databrain.core.search_engine').critical('Fallo en la conexion a brainssys.databrain.core.search_engine.get_search_engine: ', str(e))
    except ConnectionTimeout as e:
        get_logger('brainssys.databrain.core.search_engine').critical('Tiempo de espera terminado. Fallo en la conexion a brainssys.databrain.core.search_engine.get_search_engine: ', str(e))

def _get_apropiate_body(doc:dict) -> dict:
    bucket = doc.get('bucket', None)
    object_name = doc.get('object_name', None)
    dic:dict = {"query": { "bool": { } } }

    if bucket and not object_name:
        dic['query']['bool'] = {
            "must": {
                        "term": {
                            "bucket": bucket
                        }
                    }
        }
        return dic

    if object_name and not bucket:
        dic['query']['bool'] = {
            "must": {
                        "term": {
                            "object_name": object_name
                        }
                    }
        }
        return dic

    if bucket and object_name:
        dic['query']['bool'] = {
            "must": {
                        "term": {
                            "bucket": bucket
                        }
                    },
            "must": {
                        "term": {
                            "object_name": object_name
                        }
                    }
        }
        return dic
    else:
        return None
        
#empty index to do the operation in all index
def search_document(document:dict, index:str = ""):
    try:
        search:Elasticsearch = get_search_engine()
        body = _get_apropiate_body(document)
        if not body:
            raise Exception('No se puede buscar en un documento vacío')

        results:ObjectApiResponse = search.search(index=index, body=body)
        # returns = []
        # for i in range(0, len(results['hits']['hits'])):
        #     returns.append(results['hits']['hits'][i]['_source'])

        get_logger('brainssys.databrain.core.search_engine').info("Busqueda realizada con exito en el index: " + index + ". Coincidencias para el objeto: " + str(document.get('object_name', None)) + " con " + str(results['hits']['total']['value']) + " cohincidencias")
        return results

    except BadRequestError as e:
        get_logger('brainssys.databrain.core.search_engine').critical('Fallo en la conexion a brainssys.databrain.core.search_engine.search_document: ', str(e))
    except NotFoundError as e:
        get_logger('brainssys.databrain.core.search_engine').critical('Fallo en la conexion a brainssys.databrain.core.search_engine.search_document: ', str(e))
    except TransportError as e:
        get_logger('brainssys.databrain.core.search_engine').critical('Fallo en la conexion a brainssys.databrain.core.search_engine.search_document: ', str(e))


def index_document(index:str, document:dict, id:str) -> None:
    try:
        search:Elasticsearch = get_search_engine()
        search.index(index = index, document = document, id = id)
        get_logger('brainssys.databrain.core.search_engine').info("Documento indexado a ElasticSearch llamado: " + str(document.get('object_name', None))  + " con id: " + str(id))
    except BadRequestError as e:
        get_logger('brainssys.databrain.core.search_engine').critical('Fallo en la conexion a brainssys.databrain.core.search_engine.index_document: ', str(e))
    except NotFoundError as e:
        get_logger('brainssys.databrain.core.search_engine').critical('Fallo en la conexion a brainssys.databrain.core.search_engine.index_document: ', str(e))
    except TransportError as e:
        get_logger('brainssys.databrain.core.search_engine').critical('Fallo en la conexion a brainssys.databrain.core.search_engine.index_document: ', str(e))

def update_document(index:str, document:dict, id:str) -> None:
    try:
        search:Elasticsearch = get_search_engine()
        search.update(index = index, document = document, id = id)
        get_logger('brainssys.databrain.core.search_engine').info("Documento actualizado a ElasticSearch llamado: " + str(document.get('object_name', None))  + " con id: " + str(id))
    except BadRequestError as e:
        get_logger('brainssys.databrain.core.search_engine').critical('Fallo en la conexion a brainssys.databrain.core.search_engine.update_document: ', str(e))
    except NotFoundError as e:
        get_logger('brainssys.databrain.core.search_engine').critical('Fallo en la conexion a brainssys.databrain.core.search_engine.update_document: ', str(e))
    except TransportError as e:
        get_logger('brainssys.databrain.core.search_engine').critical('Fallo en la conexion a brainssys.databrain.core.search_engine.update_document: ', str(e))

def delete_document(index:str, id:str) -> None:
    try:
        search:Elasticsearch = get_search_engine()
        search.delete(index = index, id = id)
        get_logger('brainssys.databrain.core.search_engine').info("Documento eliminado a ElasticSearch con el id: " + str(id))
    except BadRequestError as e:
        get_logger('brainssys.databrain.core.search_engine').critical('Fallo en la conexion a brainssys.databrain.core.search_engine.delete_document: ', str(e))
    except NotFoundError as e:
        get_logger('brainssys.databrain.core.search_engine').critical('Fallo en la conexion a brainssys.databrain.core.search_engine.delete_document: ', str(e))
    except TransportError as e:
        get_logger('brainssys.databrain.core.search_engine').critical('Fallo en la conexion a brainssys.databrain.core.search_engine.delete_document: ', str(e))
