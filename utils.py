





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


def connect_to_gcp_bucket(bucket_name):
    '''
    Connects to google cloud storage bucket.\n
    \n
    Use in global scope to allow serverless functions to remain open while instances are spun up.
    '''
    from google.cloud import storage
    
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    return bucket


def connect_to_aws_bucket(bucket_name):
    return

def connect_to_azure_bucket(bucket_name):
    return







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

    def receiveConfirmation(self):
        raise NotImplementedError("Subclasses must implement receiveConfirmation()")

    def updateStatus(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement updateStatus()")

    def run(self):
        raise NotImplementedError("Subclasses must implement run()")



