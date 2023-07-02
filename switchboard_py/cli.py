import argparse
from .utils import start_project

def main():
    parser = argparse.ArgumentParser(prog='cloud-switchboard', description='Cloud-SwitchBoard Command-Line Interface')
    subparsers = parser.add_subparsers(dest='command')

    start_project_parser = subparsers.add_parser('start_project', help='Create a new project')
    start_project_parser.add_argument('project_name', help='Name of the project')
    start_project_parser.add_argument('cloud_provider', help='Cloud Provider being used')

    args = parser.parse_args()

    if args.command == 'start_project':
        start_project(args.project_name, args.cloud_provider)


if __name__ == '__main__':
    main()
