


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



