from google.cloud.storage.bucket import Bucket as GCP_Bucket






class CloudType:
    '''
    Base class for establishing cloud provider types.
    '''
    def __init__(self) -> None:
        self.name = self.__class__.__name__


class GCP(CloudType):
    '''
    Google Cloud Platform
    '''
    def __init__(self) -> None:
        super().__init__()

# class AWS(CloudType):
    # '''
    # Amazon Web Services
    # '''
#     def __init__(self) -> None:
#         super().__init__()

# class AZURE(CloudType):
    # '''
    # Microsoft Azure
    # '''
#     def __init__(self) -> None:
#         super().__init__()






class CloudProvider:
    '''
    Base class for establishing all methods needed for the SwitchBoard, agnostic of the cloud provider.\n
    \n
    Methods: \n
    grabStatus, grabDestination, forwardCall, receiveConfirmation, updateStatus, run
    '''
    def grabStatus(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement grabStatus()")

    def grabDestination(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement grabDestination()")

    def forwardCall(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement forwardCall()")

    def updateStatus(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement updateStatus()")









def http_trigger(func):
    '''
    Decorator for sending response immediately once http function is triggered.\n
    \n
    This alters the function so that a response is returned prior to the execution of the function.
    '''
    def trigger(request):
        import functions_framework
        
        #google cloud functions utilize the functions_framework
        @functions_framework.http
        def send_response(request):
            return 'OK'
        
        # send response prior to executing function
        send_response(request)
        func(request)

    return trigger


def init_log():
    import logging
    
    logger = logging.getLogger()
    if logger.hasHandlers():
        if logger.getEffectiveLevel() > logging.NOTSET:
            return
        else:
            logger.getLogger().setLevel(logging.INFO)
    else:    
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def connect_to_bucket(cloud_provider: GCP, bucket_name: str = 'StatusController') -> GCP_Bucket:
    '''
    Connects to cloud providers object storage bucket.\n
    \n
    Use in global scope of serverless functions to allow connection to remain open while instances are spun up.
    \n
    ARGS:\n
        cloud_provider: Currently only :class:`GCP` is supported
        bucket_name: Default `'StatusController'`, name of object storage bucket 
    '''
    if cloud_provider is GCP:

        from google.cloud import storage
        
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        return bucket

    # elif cloud_provider == 'AWS':
    #     return

    # elif cloud_provider == 'AZURE':
    #     return

    else:
        raise ValueError(f'''{cloud_provider} is not a valid cloud provider option.''')



















if __name__ == '__main__':
    connect_to_bucket(GCP, 'bucket')






