import requests
from .utils import init_log




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








