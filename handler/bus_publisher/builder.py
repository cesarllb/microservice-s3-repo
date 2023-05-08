from kink import inject
from typing import Dict
from .bus import PublisherBuss
from .interfaces.bus_publisher import IBusPublisher
from .interfaces.operations import IRemover, IUploader, IUpdater, IRemoveBucket, IMakeBucket


def buss()->IBusPublisher:
    buss = PublisherBuss()
    
    @buss.handler('brainssys.datebrain.publisher.' + 'UploadOperation')
    @inject
    def upload(payload:Dict, id, repo: IUploader):
        return repo.upload_obj(
            bucket = payload['opp']['bucket'],
            id = id,
            object_name = payload['opp']['object_name']
            )

    @buss.handler('brainssys.datebrain.publisher.' + 'UpdateOperation')
    @inject
    def update(payload:Dict, id, repo: IUpdater):
        return repo.update_obj(
            bucket = payload['opp']['bucket'],
            id = id,
            object_name = payload['opp']['object_name']
            )

    @buss.handler('brainssys.datebrain.publisher.' + 'RemoveOperation')
    @inject
    def remove(payload:Dict, id, repo: IRemover):
        return repo.remove_obj(
            bucket = payload['opp']['bucket'],
            id = id,
            object_name = payload['opp']['object_name']
            )
    
    @buss.handler('brainssys.datebrain.publisher.' + 'MakeBucketOperation')
    @inject
    def make_bucket(payload:Dict, id, repo: IMakeBucket):
        return repo.make_bucket(
            bucket = payload['opp']['bucket'],
            )
    
    @buss.handler('brainssys.datebrain.publisher.' + 'RemoveBucketOperation')
    @inject
    def remove_bucket(payload:Dict, id, repo: IRemoveBucket):
        return repo.remove_bucket(
            bucket = payload['opp']['bucket'],
            )

    return buss