import base64
import logging
from google.cloud.storage.bucket import Bucket as GCP_Bucket
from .utils import http_trigger, init_log
from .gcp import GCP_switchboard



# TODO
    # refactor to allow room for everything to be cloud agnostic
    # define default schema and allow custom schemas for destinationMap and StatusControllers
        # provide skeleton .json files
    # build out SwitchBoard run methods
    # build out testing mechanisms


##### best practice, SwitchBoard.destinationMap should be passed in as argument from environment variable ##### 




class SwitchBoard():
    '''
    Central control component of the SwitchBoard framework

    ARGS: 
        cloudProvider: Currently only 'GCP' is supported, future versions will support 'AWS' and 'AZURE'
        bucket: bucket where StatusController object can be found, use utls.connect_to_status_controller outside of serverless function entrypoint to define bucket variable in global scope
        payload: payload passed from Caller object, used to pass any necessary data to pipeline function
        destinationMap: ENV variable containing json structure used to map sender (self.caller) to appropriate pipeline endpoint
    _______________________________________________________________________________
        payload will need to include the following at minimum: \n
        {
            sender: '[name of sender here]', \n
            type: '[name of caller type here]', \n
            data: {[json data structure here]}
        }
 
    Sender and type will be used to map the appropriate pipeline to call based on the destinationMap and confirm if dependencies have been completed based on any statusController 
    object(s) retrieved.
    '''
    def __init__(self, cloud='GCP', bucket: GCP_Bucket=None, payload=None, destinationMap=None) -> None:

        self.cloud = self.setCloudProvider(cloud)
        self.data = base64.b64decode(payload['data']).decode('utf-8')
        self.caller = self.data['sender']
        self.caller_type = self.data['type']
        self.sc_bucket = bucket#    bucket name should always be StatusController
        # self.statusController = self.grabStatus()
        # status controller objects are only needed for data sources that have dependency requirements
        
        # {
        #       pipeline_name(pipeline_completetion[name(self.caller)][dependency][n]): {
        #           completed: true
        #       }
        # }
        self.destinationMap = destinationMap
        # {
        #       'cron'(self.caller_type): {
        #           'daily'(self.caller): {
        #               endpoint: {
        #                   name: URL,
        #                   name: URL,
        #                   name: URL
        #               }
        #           },
        #           'weekly'(self.caller): {
        #               endpoint: {
        #                   name: URL,
        #                   name: URL,
        #                   name: URL
        #               }
        #           }
        #       },
        #       'webhook'(self.caller_type): {
        #           name(self.caller): {
        #               endpoint: URL
        #           },
        #           name(self.caller): {
        #               endpoint: URL
        #           },
        #           name(self.caller): {
        #               endpoint: URL
        #           }
        #       },
        #       'pipeline_completion'(self.caller_type): {
        #           name(self.caller): {
        #               endpoint: URL,
        #               dependency: [
        #                   pipeline_1,
        #                   pipeline_2
        #               ],
        #           },
        #           name(self.caller): {
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

    def setCloudProvider(self, cloudProvider) -> GCP_switchboard:
        '''
        cloudProvider = 'GCP'
        '''
        if cloudProvider == "GCP":
            return GCP_switchboard()
        # elif cloudProvider == "AWS":
        #     return AWS_switchboard()
        # elif cloudProvider == "AZURE":
        #     return AZURE_switchboard()
        else:
            raise ValueError(f'''{cloudProvider} is not a valid cloud provider option, only {__doc__} is supported.''')

    def grabStatus(self):
        self.cloud.grabStatus(self.sc_bucket, self.destinationMap, self.caller)

    def grabDestination(self):
        self.cloud.grabDestination(self.destinationMap, self.caller_type, self.caller)

    def forwardCall(self, endpoint):
        self.cloud.forwardCall(endpoint)

    @http_trigger
    def receiveConfirmation(self):
        self.cloud.receiveConfirmation()

    def updateStatus(self):
        self.cloud.updateStatus(self.sc_bucket, self.caller)

    def run(self):
        self.cloud.run()


##SwitchBoard framework:
    ####PubSub or http call triggers GCF endpoints.
    ####Trigger endpoints will trigger SwitchBoard GCF via HTTP using Caller object.
    ####A destination map is passed to the SwitchBoard object and used to trigger appropriate pipelines via HTTP.
        ###SwitchBoard will reference .json file in cloud storage for any additional dependencies that should be considered.
        ###When a pipeline is triggered a 200 response is returned immediately to identify a successful trigger.
        ###Any debugging of failures will need logs of pipeline GCF to troubleshoot.
            ###Best practice should be to implement try/except block(s) with a failure message sent to the SwitchBoard GCF.
    ####On completion of pipeline GCF, another caller object triggers the SwitchBoard GCF to communicate successful run.
        ###If statusController object exists for a pipeline, SwitchBoard will update the .json file in cloud storage once successful pipeline run is communicated to it.


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










        ## cloud-switchboard on pypi
            ## need to register once library is ready enough
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



