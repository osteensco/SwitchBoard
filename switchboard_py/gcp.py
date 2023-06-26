
import json
import requests
import logging
from .utils import CloudProvider





class GCP_switchboard(CloudProvider):
    '''
    Google Cloud Platform SwitchBoard object.
    '''

    def __init__(self):
        super().__init__()



    def grabStatus(self, bucket, callerDict, caller) -> dict:
        
        blobs = bucket.list_blobs()

        status_controller = {}

        dependencies = callerDict['dependency']

        for blob in blobs:
            for dependency in dependencies:
                if blob.name.startswith(f'''{dependency}_StatusController''') and blob.name.endswith('.json'):
    
                    blob_content = blob.download_as_string()
                    status = json.loads(blob_content)
                    status_controller.update(status)

        if status_controller == {}:
            return None
        
        return status_controller

    def grabDestination(self, statusController, callerDict, caller):
        # determine the correct http endpoint to call from self.destinationMap
        endpoint_to_call = callerDict['endpoint']
        # determine if all dependency conditions are met based on statusController data
        if not statusController:
            return endpoint_to_call
        else:
            if statusController[caller]['completed']:
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

    
    def receiveConfirmation(self, caller):
        # called when caller is a completed pipeline function
        logging.info(f'''{caller} pipeline completed successfully''')

    
    def updateStatus(self, bucket, caller):
        # update appropriate json object in cloud storage
        blob = bucket.blob(f'''{caller}_StatusController.json''')

        if blob.exists():
            status_controller = {
                caller: {
                    'completed': True
                }
            }
            blob.upload_from_string(json.dumps(status_controller), content_type='application/json')














