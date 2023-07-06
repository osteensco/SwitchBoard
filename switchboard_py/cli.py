import argparse
from .cli_cmds import (
    start_project, 
    destinationmap_to_env, 
    read_config, 
    write_config_name,
    deployment_script
)






integrated_cloud_providers = [
    'gcp',
    # 'aws',
    # 'azure'
]



class ValidateArg(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values not in integrated_cloud_providers:
            raise ValueError(f'''Please choose from: {','.join(i for i in integrated_cloud_providers)}, Got value: {values}''')
        setattr(namespace, self.dest, values)




def main():
    parser = argparse.ArgumentParser(prog='cloud-switchboard', description='Cloud-SwitchBoard Command-Line Interface')
    subparsers = parser.add_subparsers(dest='command')

    start_project_parser = subparsers.add_parser('start_project', help='Create a new project')
    start_project_parser.add_argument('project_name', type=str, help='Name of the project')
    start_project_parser.add_argument('cloud_provider', type=str, action=ValidateArg, help='Cloud Provider being used')

    to_env_parser = subparsers.add_parser('destinationmap_to_env', help='convert destinationmap from json file to an env variable')
    to_env_parser.add_argument('destinationmap_path', type=str, help='Path of destinationmap.json')
    to_env_parser.add_argument('switchboard_dir', type=str, help='Path of switchboard function directory')
    
    deployment_script_parser = subparsers.add_parser('generate_deployment_script', help='creates a deployment script for a specified function for a specified cloud provider')
    deployment_script_parser.add_argument('function_name', type=str, help='name of the serverless function or status controller object file')
    deployment_script_parser.add_argument('function_directory', type=str, help='directory serverless function folder or status controller object file is located in')
    deployment_script_parser.add_argument('statuscontroller_bucket_name', nargs='?', type=str, help='Name of object storage bucket name')
    
    update_proj_name_parser = subparsers.add_parser('update_proj_name', help='Informs the CLI of the new project name')
    update_proj_name_parser.add_argument('new_name', type=str, help='The new name of the project')

    help_parser = subparsers.add_parser('help', help='Show help for all commands')

    #add subparser for 
        #switching/setting cloud provider


    args = parser.parse_args()


    if args.command == 'start_project':
        start_project(args.project_name, args.cloud_provider)

    elif args.command == 'destinationmap_to_env':
        config = read_config()
        project_name = config['project_name']
        destinationmap_to_env(project_name, args.destinationmap_path, args.switchboard_dir)

    elif args.command == 'generate_deployment_script':
        if not args.statuscontroller_bucket_name:
            bucket = None
        else:
            bucket = args.statuscontroller_bucket_name
        config = read_config()
        deployment_script[config['cloud_provider']](config['project_name'], args.function_name, args.function_directory, bucket)

    elif args.command == 'update_proj_name':
        write_config_name(args.new_name)

    elif args.command == 'help':
        parser.print_help()






if __name__ == '__main__':
    main()



