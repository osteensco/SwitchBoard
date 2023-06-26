import base64
import logging
from google.cloud.storage.bucket import Bucket as GCP_Bucket
from .utils import http_trigger, init_log, GCP
from .gcp import GCP_switchboard



# TODO

    # build out unit tests








class SwitchBoard():
    '''
    Central control component of the SwitchBoard framework

    ARGS: 
        cloudProvider: Currently only :class:`GCP` is supported, future versions will support :class:`AWS` and :class:`AZURE`
        bucket: bucket where StatusController object can be found, see utls.connect_to_bucket
        payload: payload passed from Caller object, used to pass any necessary data to pipeline function
        destinationMap: ENV variable containing json structure used to map sender (self.caller) to appropriate pipeline endpoint
    \n_______________________________________________________________________________\n
        payload will need to include the following at minimum: \n
        {
            caller: '[name of sender here]', \n
            type: '[name of caller type here]', \n
            data: {[json data structure here]}
        }
 
    Sender and type will be used to map the appropriate pipeline to call based on the destinationMap and confirm if dependencies have been completed based on any statusController 
    object(s) retrieved.\n
    As a best practice, destinationMap should be passed in from an environment variable
    \n_______________________________________________________________________________\n
    Example schema for destinationMap:
        {
            "cron": {
                "daily": {
                    "endpoint": {
                        "name1": "URL",
                        "name2": "URL",
                        "name3": "URL"
                    }
                },
                "weekly": {
                    "endpoint": {
                        "name4": "URL",
                        "name5": "URL",
                        "name6": "URL"
                    }
                }
            },
            "webhook": {
                "name1": {
                    "endpoint": "URL"
                },
                "name2": {
                    "endpoint": "URL"
                },
                "name3": {
                    "endpoint": "URL"
                }
            },
            "pipeline_completion": {
                "name1": {
                    "endpoint": "URL",
                    "dependency": [
                        "pipeline_name3",
                        "pipeline_name4"
                    ]
                },
                "name2": {
                    "endpoint": {
                "name1": "URL",
                "name2": "URL",
                "name3": "URL"
            },
                    "dependency": [
                        "pipeline_name5",
                        "pipeline_name6"
                    ]
                }
            }
        }
    \n_______________________________________________________________________________\n
    Example schema for a statusController:
        {
            pipeline_name(pipeline_completetion[name(self.caller)][dependency][n]): {
                completed: true
            }
        }




    '''
    def __init__(self, cloud: GCP=GCP, bucket: GCP_Bucket | None=None, payload: dict=None, destinationMap: dict=None) -> None:

        self.cloud = self.setCloudProvider(cloud)
        self.data = base64.b64decode(payload['data']).decode('utf-8')
        self.caller = self.data['caller']
        self.caller_type = self.data['type']
        self.caller_dict = destinationMap[self.caller_type][self.caller]
        self.sc_bucket = bucket#    bucket name should always be StatusController
        self.statusController = None
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


    def grabDependencies(self):
        if 'dependency' in self.caller_dict:
            return self.caller_dict['dependency']
        else:
            return None


    def checkDependencies(self, dependencies, endpoint) -> bool:
        if dependencies:
            for name in dependencies:
                if self.statusController[name]["completed"]:
                    continue
                else:
                    logging.info(f'''{endpoint} dependency not met''')
                    return False
        return True


    def setCloudProvider(self, cloudProvider: GCP) -> GCP_switchboard:
        '''
        Mapping function for cloud providers SwitchBoard is integrated with.
        '''
        if cloudProvider is GCP:
            return GCP_switchboard()
        # elif cloudProvider == "AWS":
        #     return AWS_switchboard()
        # elif cloudProvider == "AZURE":
        #     return AZURE_switchboard()
        else:
            raise ValueError(f'''{cloudProvider} is not a valid cloud provider option, only {GCP} is supported.''')



    def grabStatus(self) -> dict:
        self.cloud.grabStatus(self.sc_bucket, self.caller_dict, self.caller)

    def grabDestination(self) -> dict | str:
        self.cloud.grabDestination(self.statusController, self.caller_dict, self.caller)

    async def forwardCall(self, endpoint):
        await self.cloud.forwardCall(endpoint)

    @http_trigger
    def receiveConfirmation(self):
        self.cloud.receiveConfirmation(self.caller)

    def updateStatus(self):
        self.cloud.updateStatus(self.sc_bucket, self.caller)

    async def run(self):
        self.receiveCall()
        if self.caller_type == 'pipeline_completion':
            self.receiveConfirmation()
            self.updateStatus()

        self.statusController = self.grabStatus()
        endpoint = self.grabDestination()
        dependencies = self.grabDependencies()

        if type(endpoint) is dict:
            for key in endpoint.keys():
                if self.checkDependencies(dependencies, key):
                    await self.forwardCall(endpoint[key])
        elif type(endpoint) is str:
            if self.checkDependencies(dependencies, endpoint):
                await self.forwardCall(endpoint)
        else:
            raise TypeError(f'''{type(endpoint)} Type not supported, endpoint must be dict or str''')








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
        from .caller import Caller
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



