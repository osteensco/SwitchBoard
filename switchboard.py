import base64
import requests
import logging
import json
from google.cloud import storage
from .utils import http_trigger, init_log




# TODO
    # build out SwitchBoard methods
    ##### BUILD StatusController JSON(s) #####
    ##### SwitchBoard.destinationMap should be passed in as argument from environment variable ##### 

    # build out testing mechanisms









class Caller():
    '''
    Used for interacting with the SwitchBoard API

    ARGS:
        switchboard: ENV variable of switchboard endpoint
        sender: name of sender, used by SwitchBoard to map call to appropriate pipeline
        payload: data to be ultimately passed to pipeline function
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
    '''
    Central control component of the SwitchBoard framework

    ARGS: 
        bucket_name: name of object storage bucket where StatusController object can be found
        payload: payload passed from Caller object, used to pass any necessary data to pipeline function
        destinationMap: ENV variable containing json structure used to map sender (self.caller) to appropriate pipeline endpoint
    _______________________________________________________________________________
        payload will need to include the following at minimum:
        {
            sender: '[name of sender here]', \n
            data: {[json data structure here]}
        }
 
    Sender will be used to map the appropriate pipeline to call based on the StatusController object retrieved.
    '''
    def __init__(self, bucket_name, payload, destinationMap) -> None:
        self.data = base64.b64decode(payload['data']).decode('utf-8')
        self.caller = self.data['sender']
        self.statusController = self.grabStatus(bucket_name)
        # status controller objects are only needed for data sources that have dependency requirements
        # {
        #       pipeline_name: {
        #           completed: true
        #       }
        # }
        self.destinationMap = destinationMap
        # {
        #       'cron': {
        #           'daily': {
        #               prev_run: 'UTC Timestamp',
        #               next_run: 'UTC Timestamp',
        #               endpoint: {
        #                   name: URL,
        #                   name: URL,
        #                   name: URL
        #               }
        #           },
        #           'weekly': {
        #               prev_run: 'UTC Timestamp',
        #               next_run: 'UTC Timestamp',
        #               endpoint: {
        #                   name: URL,
        #                   name: URL,
        #                   name: URL
        #               }
        #           }
        #       },
        #       'webhook': {
        #           endpoint: {
        #               name: URL,
        #               name: URL,
        #               name: URL
        #           }
        #       },
        #       'pipeline_completion': {
        #           name: {
        #               endpoint: URL,
        #               dependency: [
        #                   pipeline_1,
        #                   pipeline_2
        #               ]
        #           },
        #           name: {
        #               endpoint: URL,
        #               dependency: [
        #                   pipeline_1,
        #                   pipeline_2
        #               ]
        #           }
        #       }
        # }
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

        dependencies = self.destinationMap['pipeline_completion'][self.caller]['dependency']

        for blob in blobs:
            for dependency in dependencies:
                if blob.name.startswith(f'''{dependency}_StatusController/''') and blob.name.endswith('.json'):
    
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

    def callDownstream(self):
        # will execute workflow steps for calling pipelines triggered by upstream completetions
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


##### Handle concurrent updates on StatusController google cloud storage objects -

        # Conditional Requests: 

            # GCS supports conditional requests that allow you to specify conditions for updates. 
            # For example, you can use the ifGenerationMatch parameter when performing an update. 
            # This parameter ensures that the update is applied only if the current generation of the object matches the one provided. 
            # If the generation does not match, it means another instance has updated the object, and you can choose to retry the update or handle the conflict accordingly.

        # Distributed Locking:

            # Acquiring a lock before updating the StatusController ensures that only one instance can modify the StatusController at a time. 
            # GCS itself doesn't provide built-in distributed locking mechanisms. I could potentially use another object as a "lock". 
            # For every object, a corresponding lock object could exist, this could be created by the SwitchBoard and contain a unique key the SwitchBoard generates in each instance. 
            # Prior to updating the StatusController, a short pause is executed and the lock is verified with the unique instance key.
            # If key does not match, SwitchBoard applies retry logic after a certain amount of time.
            # Upon SwitchBoard completion, it's lock is removed. 
        
        # Atomic Operations: 

            # Instead of directly updating the entire StatusController, you can update specific fields. 
            # By using atomic operations supported by GCS (e.g., compose operation), Cloud Function instances can modify specific fields independently, reducing the likelihood of conflicts.









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



