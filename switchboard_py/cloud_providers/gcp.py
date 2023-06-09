
import json
import requests
import logging
from google.cloud.storage.bucket import Bucket
from .cloud_types import CloudProvider






class GCP_switchboard(CloudProvider):
    '''
    Google Cloud Platform SwitchBoard object.
    '''

    def __init__(self):
        super().__init__()



    def grabStatus(self, bucket, callerDict, dependencyKey) -> dict:
        
        blobs = bucket.list_blobs()

        status_controller = {}

        dependencies = callerDict[dependencyKey]

        for blob in blobs:
            for dependency in dependencies:
                if blob.name.startswith(f'''{dependency}''') and blob.name.endswith('.json'):
    
                    blob_content = blob.download_as_string()
                    status = json.loads(blob_content)
                    status_controller.update(status)

        if status_controller == {}:
            return None
        
        return status_controller

    def grabDestination(self, statusController, callerDict, caller, completedStatusKey, endpointKey):
        # determine the correct http endpoint to call from self.destinationMap
        endpoint_to_call = callerDict[endpointKey]
        # determine if all dependency conditions are met based on statusController data
        if not statusController:
            return endpoint_to_call
        else:
            if statusController[caller][completedStatusKey]:
                return endpoint_to_call
            else:
                return None

    async def forwardCall(self, endpoint):
        # send request(s) to identified http endpoint(s) and pass along any relevant data
        response = await requests.post(endpoint, json=self.data)

        if response.status_code == 200:
            logging.info('Pipeline trigger request successful!')
        else:
            logging.error('Pipeline trigger request failed with status code:', response.status_code)

    def updateStatus(self, bucket: Bucket, caller: str, completedStatusKey: str, status: bool):
        # update appropriate json object in cloud storage
        blob = bucket.blob(f'''{caller}.json''')

        if blob.exists():
            status_controller = {
                caller: {
                    completedStatusKey: status
                }
            }
            blob.upload_from_string(json.dumps(status_controller), content_type='application/json')














