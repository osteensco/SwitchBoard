from google.cloud.storage.bucket import Bucket as GCP_Bucket
import os





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









def http_trigger(func):
    '''
    Decorator for sending response immediately once http function is triggered.\n
    \n
    This alters the function so that a response is returned prior to the execution of the function.
    '''
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
    import logging
    
    logger = logging.getLogger()
    if logger.hasHandlers():
        if logger.getEffectiveLevel() > logging.NOTSET:
            return
        else:
            logger.getLogger().setLevel(logging.INFO)
    else:    
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def connect_to_bucket(cloud_provider: GCP, bucket_name: str = 'StatusController') -> GCP_Bucket:
    '''
    Connects to cloud providers object storage bucket.\n
    \n
    Use in global scope of serverless functions to allow connection to remain open while instances are spun up.
    \n
    ARGS:\n
        cloud_provider: Currently only :class:`GCP` is supported
        bucket_name: Default `'StatusController'`, name of object storage bucket 
    '''
    if cloud_provider is GCP:

        from google.cloud import storage
        
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        return bucket

    # elif cloud_provider == 'AWS':
    #     return

    # elif cloud_provider == 'AZURE':
    #     return

    else:
        raise ValueError(f'''{cloud_provider} is not a valid cloud provider option.''')






def endpoint_boilerplate():
    return '''
import os
from cloud-switchboard import http_trigger, Caller

@http_trigger
def main(request):
    
    #do some data stuff

    sb_endpoint = os.environ.get('SWITCHBOARD')
    caller_name = 'endpoint_boilerplate'
    caller_type = 'cron'
    payload = {'datafield': 'some data'}

    call_switchboard = Caller(sb_endpoint, caller_name, caller_type, payload)
    call_switchboard.invoke()
    '''


def pipeline_boilerplate():
    return '''
import os
from cloud-switchboard import http_trigger, Caller

@http_trigger
def main(request):
    
    #do some data stuff

    sb_endpoint = os.environ.get('SWITCHBOARD')
    caller_name = 'pipeline_boilerplate'
    caller_type = 'pipeline_completetion'
    payload = {'datafield': 'some data'}

    send_conf_message = Caller(sb_endpoint, caller_name, caller_type, payload)
    send_conf_message.invoke()
    '''


def switchboard_boilerplate():
    return '''
from cloud-switchboard import http_trigger, SwitchBoard, connect_to_bucket, GCP

bucket = connect_to_bucket(GCP)

@http_trigger
def main(request):

    payload = {'datafield': 'some data'}
    destinationMap = os.environ.get('DESTINATIONMAP')

    sb = SwitchBoard(GCP, bucket, payload, destinationMap)
    sb.run()

    '''


def destinationmap_boilerplate():
    return '''
{
    "cron": {
        "daily": {
            "endpoint": {
                "name1": "URL",
                "name2": "URL",
                "name3": "URL"
            }
        },
        "endpoint_boilerplate": {
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
        "pipeline_boilerplate": {
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
    '''






def create_api(project_manager_api):

    code = '''
#!/usr/bin/env python
from cloud-switchboard.project_manager import api

if __name__ == '__main__':
    # code here
'''
    #map out commands for deploying functions and StatusController objects.
    #other commands could include
        #switching/setting cloud provider
        #creating .yaml files for specific pipelines
        #deploy StatusController files to object storage
        #various other tasks

    with open(project_manager_api, 'w') as f:
        f.write(code)


def create_gcp_deployment_scripts(project_dir):

    buildd_dir = 'cloud_builds'
    dir_path = os.path.join(project_dir, buildd_dir)
    os.makedirs(dir_path, exist_ok=True)

    cloudbuild_file = os.path.join(project_dir, buildd_dir, 'switchboard.yaml')
    build_steps = '''
steps:
- name: 'gcr.io/cloud-builders/gcloud'
  args:
  - functions
  - deploy
  - main
  - --source=./switchboard
  - --trigger-http
  - --allow-unauthenticated
  - --runtime=python39
  - --memory=1024MB
  - --timeout=540s
'''
    with open(cloudbuild_file, 'w') as yaml:
        yaml.write(build_steps)


def create_aws_deployment_scripts(project_dir):
    return


def create_azure_deployment_scripts(project_dir):
    return


deployment_script = {
    'gcp': create_gcp_deployment_scripts,
    # 'aws': create_aws_deployment_scripts,
    # 'azure': create_azure_deployment_scripts
}


def start_project(project_name, cloud_provider):

    base_dir = os.getcwd()
    project_dir = os.path.join(base_dir, project_name)

    # Create the main project directory
    os.makedirs(project_dir, exist_ok=True)

    # Create subdirectories and files
    subdirectories = [
        'switchboard',
        'endpoints',
        'pipelines',
        'statuscontroller'
    ]

    for subdir in subdirectories:
        dir_path = os.path.join(project_dir, subdir)
        os.makedirs(dir_path, exist_ok=True)

    deployment_script[cloud_provider](project_dir)
    
    endpoint = os.path.join(project_dir, 'endpoints', 'endpoint_placeholder.py')
    pipeline = os.path.join(project_dir, 'pipelines', 'pipeline_placeholder.py')
    switchboard_py = os.path.join(project_dir, 'switchboard', 'switchboard.py')
    destination_map = os.path.join(project_dir, 'switchboard', 'destinationMap.json')
    project_manager_api = os.path.join(project_dir, 'manager_api.py')

    
    with open(endpoint, 'w') as e:
        e.write(endpoint_boilerplate())
    with open(pipeline, 'w') as p:
        p.write(pipeline_boilerplate())
    with open(switchboard_py, 'w') as s:
        s.write(switchboard_boilerplate())
    with open(destination_map, 'w') as d:
        d.write(destinationmap_boilerplate())
    create_api(project_manager_api)


    print(f"Project directory '{project_name}' created successfully!")
    print(f"Cloud provider set as: {cloud_provider}")


















if __name__ == '__main__':
    connect_to_bucket(GCP, 'bucket')






