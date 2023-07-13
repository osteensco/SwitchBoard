import os
import json






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
    payload = request_body = request.get_json()

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
    
    request_body = request_body = request.get_json()

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
    payload = request.get_json()
    destinationMap = os.environ.get('DESTINATIONMAP')

    sb = SwitchBoard(GCP, bucket, payload, destinationMap)
    sb.run()

    '''


def destinationmap_boilerplate():
    return """DESTINATIONMAP={"cron": {"daily": {"endpoint": {"name1": "URL", "name2": "URL", "name3": "URL"}}, "endpoint_boilerplate": {"endpoint": {"name4": "URL", "name5": "URL", "name6": "URL"}}}, "webhook": {"name1": {"endpoint": "URL"}, "name2": {"endpoint": "URL"}, "name3": {"endpoint": "URL"}}, "pipeline_completion": {"pipeline_boilerplate": {"endpoint": "URL", "dependency": ["pipeline_name3", "pipeline_name4"]}, "name2": {"endpoint": {"name1": "URL", "name2": "URL", "name3": "URL"}, "dependency": ["pipeline_name5", "pipeline_name6"]}}}"""


def env_boilerplate():
    return """SWITCHBOARD='switchboard function endpoint url here'"""


def get_proj_dir_path(project_name):
    base_dir = os.getcwd()
    project_dir = os.path.join(base_dir, project_name)
    return project_dir


def create_gcp_deployment_script(project_name, function_name, func_directory, statuscontroller_bucket_name=None):

    project_dir = get_proj_dir_path(project_name)
    buildd_dir = 'cloud_builds'
    dir_path = os.path.join(project_dir, buildd_dir)
    os.makedirs(dir_path, exist_ok=True)


    cloudbuild_file = os.path.join(project_dir, buildd_dir, f'''{function_name}.yaml''')
    
    if function_name != func_directory:
        path = f'''./{func_directory}/{function_name}'''
    else:
        path = f'''./{function_name}'''


    if '.json' in function_name.lower():
        build_steps = f'''
steps:
- name: 'gcr.io/cloud-builders/gsutil'
  args: ['cp', '{path}', 'gs://{statuscontroller_bucket_name}']
        '''

    else:
        build_steps = f'''
steps:
- name: 'gcr.io/cloud-builders/gcloud'
  args:
  - functions
  - deploy
  - main
  - --source={path}
  - --trigger-http
  - --allow-unauthenticated
  - --runtime=python39
  - --memory=1024MB
  - --timeout=540s
'''

    with open(cloudbuild_file, 'w') as yaml:
        yaml.write(build_steps)

    print(f'''Created {cloudbuild_file}''')



def create_aws_deployment_script(project_dir):
    return


def create_azure_deployment_script(project_dir):
    return



deployment_script = {
    'gcp': create_gcp_deployment_script,
    # 'aws': create_aws_deployment_script,
    # 'azure': create_azure_deployment_script
}


def read_config():
    base_dir = os.getcwd()
    config = os.path.join(base_dir, 'config.json')
    with open(config, 'r') as c:
        settings = json.loads(c.read())
    return settings


def write_config_name(new_project_name):
    config = read_config()
    proj_dir = config['project_name']
    cloud_provider = config['cloud_provider']

    os.rename(proj_dir, new_project_name)
    create_config(new_project_name, cloud_provider)
    

    print(f'''Project name updated to {new_project_name}''')


def create_config(project_name, cloud_provider):
    base_dir = os.getcwd()
    config = os.path.join(base_dir, 'config.json')

    with open(config, 'w') as c:
        proj_info = {
            "project_name": f"{project_name}",
            "cloud_provider": f"{cloud_provider}"
        }
        c.write(json.dumps(proj_info))


def start_project(project_name, cloud_provider):

    project_dir = get_proj_dir_path(project_name)

    # Create the main project directory
    os.makedirs(project_dir, exist_ok=True)

    # Create subdirectories and files
    subdirectories = [
        'switchboard',
        'endpoints/endpoint_placeholder',
        'pipelines/pipeline_placeholder',
        'statuscontroller'
    ]

    for subdir in subdirectories:
        dir_path = os.path.join(project_dir, subdir)
        os.makedirs(dir_path, exist_ok=True)

    
    endpoint = os.path.join(project_dir, 'endpoints', 'endpoint_placeholder', 'main.py')
    endpoint_env = os.path.join(project_dir, 'endpoints', 'endpoint_placeholder', 'sb_endpoint.env')
    pipeline = os.path.join(project_dir, 'pipelines', 'pipeline_placeholder', 'main.py')
    pipeline_env = os.path.join(project_dir, 'pipelines', 'pipeline_placeholder', 'sb_endpoint.env')
    switchboard_py = os.path.join(project_dir, 'switchboard', 'main.py')
    destination_map = os.path.join(project_dir, 'switchboard', 'destinationMap.env')
    statuscontroller = os.path.join(project_dir, 'statuscontroller', 'example.json')

    deployment_script[cloud_provider](project_dir, 'endpoint_placeholder', 'endpoints')
    deployment_script[cloud_provider](project_dir, 'pipeline_placeholder', 'pipelines')
    deployment_script[cloud_provider](project_dir, 'switchboard', 'switchboard')

    create_config(project_name, cloud_provider)
    print('project config file created')

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

    with open(statuscontroller, 'w') as st:
        st.write('''
{
    "pipeline_name": {
        "completed": false
    }
}
        ''')
    print('StatusController example object created')


    print(f"Project directory '{project_name}' created successfully!")
    print(f"Cloud provider set as: {cloud_provider}")



def destinationmap_to_env(project_name, destinationmap_path, switchboard_dir):

    project_dir = get_proj_dir_path(project_name)
    destinationmap = os.path.join(project_dir, destinationmap_path)

    with open(destinationmap, 'r') as json_file:
        data = json.load(json_file)
    
    json_string = json.dumps(data, separators=(',', ':'))
    json_string = json_string.replace('\n', '')

    switchboard_directory = os.path.join(project_dir, switchboard_dir)
    env_file = os.path.join(switchboard_directory, 'destinationMap.env')
    with open(env_file, 'w') as env_file:
        env_file.write("DESTINATIONMAP=" + json_string)

    print('Destination map json converted to env file')






if __name__ == '__main__':
    base_dir = os.getcwd()
    project_dir = os.path.join(base_dir, 'project_name')
    print('')
    print(os.path.join(project_dir, 'pipelines', 'pipeline_placeholder', 'sb_endpoint.env'))
    pass

