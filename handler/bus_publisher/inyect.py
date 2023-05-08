from kink import di
from bus_publisher.repository import Upload, Update, Remove, MakeBucket, RemoveBucket
from bus_publisher.interfaces.operations import IUploader, IUpdater, IRemover, IMakeBucket, IRemoveBucket

def config():
    di[IUploader] = Upload()
    di[IUpdater] = Update()
    di[IRemover] = Remove()
    di[IMakeBucket] = MakeBucket()
    di[IRemoveBucket] = RemoveBucket()