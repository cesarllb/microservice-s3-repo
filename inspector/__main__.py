from kink import di
from fastapi import FastAPI
from api.confi_inspector import config
from api.endpoints import repo
from core.logger import get_logger

def app()->FastAPI:
    config()
    fapp = FastAPI(title="brainssys.databrain.inspector", description="Componente para consultar a MinIO y a Elasticsearch y recibir información sobre las neuroimágenes.", version='0.1.0')
    fapp.include_router(repo)
    return fapp

if __name__ =='__main__':
    import uvicorn

    try:
        uvicorn.run(
                app(), 
                host = di['INSPECTOR_INTERFACE_HOST'], 
                port = int(di['INSPECTOR_INTERFACE_PORT']))
    except:
        get_logger('brainssys.databrain.inspector').error("Fallo de FastAPI Inspector en el puerto " + di['INSPECTOR_INTERFACE_PORT'] +
        " y el host " + di['INSPECTOR_INTERFACE_HOST'])

