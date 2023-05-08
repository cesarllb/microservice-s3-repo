from kink import di
from fastapi import FastAPI
from core.logger import get_logger
from api.endpoints import repo
from api.confi_publisher import boostrap

def app()->FastAPI:
    fapp = FastAPI(title="brainssys.databrain.publisher", description="Componente para crear y enviar eventos a Kafka", version='0.1.0')
    fapp.include_router(repo)
    return fapp

if __name__ =='__main__':
    import uvicorn

    boostrap()
    try:
        uvicorn.run(
                app(), 
                host= di['PUBLISHER_INTERFACE_HOST'], 
                port= int(di['PUBLISHER_INTERFACE_PORT'])
                )
    except:
        get_logger('brainssys.databrain.core.publisher').error("Fallo de FastAPI Publisher en el puerto " + di['PUBISHER_INTERFACE_PORT'] +
        " y el host " + di['PUBLISHER_INTERFACE_HOST'])





    