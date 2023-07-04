import os





def endpoint_boilerplate():
    return '''
import os
from dotenv import load_dotenv
from switchboard_py import http_trigger, Caller

@http_trigger
def main(request):
    
    #do some data stuff

    load_dotenv('sb_endpoint.env')
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
from dotenv import load_dotenv
from switchboard_py import http_trigger, Caller

@http_trigger
def main(request):
    
    #do some data stuff

    load_dotenv('sb_endpoint.env')
    sb_endpoint = os.environ.get('SWITCHBOARD')
    caller_name = 'pipeline_boilerplate'
    caller_type = 'pipeline_completetion'
    payload = {'datafield': 'some data'}

    send_conf_message = Caller(sb_endpoint, caller_name, caller_type, payload)
    send_conf_message.invoke()
    '''


def switchboard_boilerplate():
    return '''
import os
from dotenv import load_dotenv
from switchboard_py import http_trigger, SwitchBoard, connect_to_bucket, GCP

bucket = connect_to_bucket(GCP)

@http_trigger
def main(request):

    load_dotenv('destinationMap.env')
    payload = {'datafield': 'some data'}
    destinationMap = os.environ.get('DESTINATIONMAP')

    sb = SwitchBoard(GCP, bucket, payload, destinationMap)
    sb.run()

    '''


def destinationmap_boilerplate():
    return """DESTINATIONMAP={"cron": {"daily": {"endpoint": {"name1": "URL", "name2": "URL", "name3": "URL"}}, "endpoint_boilerplate": {"endpoint": {"name4": "URL", "name5": "URL", "name6": "URL"}}}, "webhook": {"name1": {"endpoint": "URL"}, "name2": {"endpoint": "URL"}, "name3": {"endpoint": "URL"}}, "pipeline_completion": {"pipeline_boilerplate": {"endpoint": "URL", "dependency": ["pipeline_name3", "pipeline_name4"]}, "name2": {"endpoint": {"name1": "URL", "name2": "URL", "name3": "URL"}, "dependency": ["pipeline_name5", "pipeline_name6"]}}}"""


def env_boilerplate():
    return """SWITCHBOARD='switchboard function endpoint url here'"""


def create_gcp_deployment_scripts(project_dir, function_name, func_directory):

    buildd_dir = 'cloud_builds'
    dir_path = os.path.join(project_dir, buildd_dir)
    os.makedirs(dir_path, exist_ok=True)

    cloudbuild_file = os.path.join(project_dir, buildd_dir, f'''{function_name}.yaml''')
    build_steps = f'''
steps:
- name: 'gcr.io/cloud-builders/gcloud'
  args:
  - functions
  - deploy
  - main
  - --source=./{func_directory}/{function_name}
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

    
    endpoint = os.path.join(project_dir, 'endpoints/endpoint_placeholder', 'main.py')
    endpoint_env = os.path.join(project_dir, 'endpoints/endpoint_placeholder', 'sb_endpoint.env')
    pipeline = os.path.join(project_dir, 'pipelines/pipeline_placeholder', 'main.py')
    pipeline_env = os.path.join(project_dir, 'pipelines/pipeline_placeholder', 'sb_endpoint.env')
    switchboard_py = os.path.join(project_dir, 'switchboard', 'main.py')
    destination_map = os.path.join(project_dir, 'switchboard', 'destinationMap.env')

    deployment_script[cloud_provider](project_dir, 'endpoint_placeholder', 'endpoints')
    deployment_script[cloud_provider](project_dir, 'pipeline_placeholder', 'pipelines')
    deployment_script[cloud_provider](project_dir, 'switchboard', 'switchboard')

    
    with open(endpoint, 'w') as e:
        e.write(endpoint_boilerplate())
    with open(endpoint_env, 'w') as ee:
        ee.write(env_boilerplate())
    print('enpoint boilerplate function created')

    with open(pipeline, 'w') as p:
        p.write(pipeline_boilerplate())
    with open(pipeline_env, 'w') as ep:
        ep.write(env_boilerplate())
    print('pipeline boilerplate function created')

    with open(switchboard_py, 'w') as s:
        s.write(switchboard_boilerplate())
    print('switchboard boilerplate function created')

    with open(destination_map, 'w') as d:
        d.write(destinationmap_boilerplate())
    print('destinationMap boilerplate schema created')


    print(f"Project directory '{project_name}' created successfully!")
    print(f"Cloud provider set as: {cloud_provider}")





if __name__ == '__main__':
    pass
