from google.cloud import storage




#decorator for sending response immediately once http function is triggered
def http_trigger(func):
    
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


def connect_to_status_controller(bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    return bucket


