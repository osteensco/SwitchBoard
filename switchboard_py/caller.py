import requests
import logging








class Caller():
    '''
    Used for interacting with the SwitchBoard API

    ARGS:
        switchboard: ENV variable of switchboard endpoint
        caller: name of caller, used by SwitchBoard to map call to appropriate pipeline using the destinationMap
        callerType: type of caller, used by SwitchBoard to map call to appropriate pipeline using the destinationMap
        payload: data to be ultimately passed to pipeline function
    '''
    def __init__(self, switchboard, caller, callerType, payload) -> None:
        self.switchboard_ep = switchboard
        self.body = payload
        self.caller = caller
        self.caller_type = callerType
        self.payload = self.constructPayload(caller, callerType, payload)


    def constructPayload(self, caller, callerType, body):
        return {
            'caller': caller,
            'type': callerType,
            'data': body
        }

    def invoke(self):
        response = requests.post(self.switchboard, json=self.payload)

        if response.status_code == 200:
            logging.info('Switchboard trigger request successful!')
        else:
            logging.error('Request failed with status code:', response.status_code)










