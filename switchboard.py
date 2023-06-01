import base64
import requests
import logging
import json
from google.cloud import storage



# TODO
    # build out SwitchBoard methods
    # build out testing mechanisms









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
    logger = logging.getLogger()
    if logger.hasHandlers():
        if logger.getEffectiveLevel() > logging.NOTSET:
            return
        else:
            logger.getLogger().setLevel(logging.INFO)
    else:    
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)










class Caller():
    '''
    Used for interacting with the SwitchBoard API
    '''
    def __init__(self, switchboard, sender, payload) -> None:
        self.switchboard = switchboard
        self.payload = payload
        self.payload['sender'] = sender
        init_log()

    def place_call(self):
        print('call placed to switchboard')
        # response = requests.post(self.switchboard, json=self.body)

        # if response.status_code == 200:
        #     logging.info('Switchboard trigger request successful!')
        # else:
        #     logging.error('Request failed with status code:', response.status_code)




class SwitchBoard():
    
    def __init__(self, bucket_name, data) -> None:
        self.data = base64.b64decode(data['data']).decode('utf-8')
        self.caller = self.data['sender']
        self.statusController = self.grabStatus(bucket_name)
        self.destinationMap = {
            'cron': [],
            'webhook': [],

        }
        init_log()

    @http_trigger
    def receiveCall(self):
        logging.info(f'''Call received from {self.caller}''')
        return

    def grabStatus(self, bucket_name):
        # read in appropriate json object in cloud storage
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)

        blobs = bucket.list_blobs()

        status_controller = {}
        # status_controller = []

        for blob in blobs:
            if blob.name.startswith(f'''{self.caller}/''') and blob.name.endswith('.json'):
 
                blob_content = blob.download_as_text()
                status = json.loads(blob_content)
                status_controller.update(status)
                # status_controller.append(status)
        return status_controller

    def grabDestination(self):
        # determine the correct http endpoint to call from self.destinationMap
        # determine if all dependency conditions are met based on statusController data
        return

    def forwardCall(self):
        # send request(s) to identified http endpoint(s)
        # pass along any relevant data
        return

    def receiveConfirmation(self):
        # called when caller is a completed pipeline function
        return
    
    def updateStatus(self):
        # update appropriate json object in cloud storage
        return






##SwitchBoard framework:
    ####PubSub triggers GCF endpoints.
    ####Trigger endpoints will trigger SwitchBoard GCF via HTTP.
    ####SwitchBoard contains graph data structure that will trigger appropriate pipelines via HTTP.
        ###SwitchBoard will reference .json file in cloud storage for any additional dependencies that should be considered.
        ###When a pipeline is triggered a 200 response is returned immediately to identify a successful trigger.
        ###Any failures will exist in logs of pipeline GCF.
    ####On completion of pipeline GCF, SwitchBoard will be triggered to communicate successful run.
        ###SwitchBoard will update .json file in cloud storage once successful pipeline run is communicated to it.

    # need to setup SwitchBoard library
        ## git+https://github.com/osteensco/[SwitchBoard].git
        ## pip install -e
            ## this will install the library in "editable mode" allowing changes to the library to be reflected automatically



if __name__ == '__main__':
    
    
    # I probably won't need to use http_trigger decorator for entrypoint functions as I leverage pubsub messages instead of HTTP triggers here.
    # The SwitchBoard is always HTTP triggered though.
    # @http_trigger
    def entrypoint(request):
        sender = 'daily'
        payload = {'headers': {'APIKEY': '12345'}, 'body':  request['body']}
        caller = Caller(
            switchboard='switchboard',
            sender=sender,
            payload=payload
            )
        print(caller.payload)
        caller.place_call()

    entrypoint({'headers': 'none', 'body': 'some data here'})



