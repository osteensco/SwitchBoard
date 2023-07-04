import argparse
from .cli_cmds import start_project


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
    #add subparser for 
        #convert destinationMap .json to .env
        #writing .yaml for a specific function directory
        #switching/setting cloud provider
        #upload StatusController files to object storage
        #???
    start_project_parser.add_argument('project_name', type=str, help='Name of the project')
    start_project_parser.add_argument('cloud_provider', type=str, action=ValidateArg, help='Cloud Provider being used')

    args = parser.parse_args()

    if args.command == 'start_project':
        start_project(args.project_name, args.cloud_provider)


if __name__ == '__main__':
    main()



