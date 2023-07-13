





class CloudType:
    '''
    Base class for establishing cloud provider types.
    '''
    def __init__(self) -> None:
        self.name = self.__class__.__name__


class GCP(CloudType):
    '''
    Google Cloud Platform
    '''
    def __init__(self) -> None:
        super().__init__()


# class AWS(CloudType):
    # '''
    # Amazon Web Services
    # '''
#     def __init__(self) -> None:
#         super().__init__()


# class AZURE(CloudType):
    # '''
    # Microsoft Azure
    # '''
#     def __init__(self) -> None:
#         super().__init__()






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

    def updateStatus(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement updateStatus()")

