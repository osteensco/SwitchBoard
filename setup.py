from setuptools import setup, find_packages

setup(
    name='cloud-switchboard',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'blinker>=1.6.2',
        'cachetools>=5.3.1',
        'certifi>=2023.5.7',
        'charset-normalizer>=3.1.0',
        'click>=8.1.3',
        'cloudevents>=1.9.0',
        'colorama>=0.4.6',
        'deprecation>=2.1.0',
        'Flask>=2.3.2',
        'functions-framework>=3.4.0',
        'google-api-core>=2.11.0',
        'google-auth>=2.19.1',
        'google-cloud-core>=2.3.2',
        'google-cloud-storage>=2.9.0',
        'google-crc32c>=1.5.0',
        'google-resumable-media>=2.5.0',
        'googleapis-common-protos>=1.59.0',
        'idna>=3.4',
        'itsdangerous>=2.1.2',
        'Jinja2>=3.1.2',
        'MarkupSafe>=2.1.2',
        'numpy>=1.24.3',
        'packaging>=23.1',
        'pandas>=2.0.2',
        'protobuf>=4.23.2',
        'pyasn1>=0.5.0',
        'pyasn1-modules>=0.3.0',
        'python-dateutil>=2.8.2',
        'pytz>=2023.3',
        'requests>=2.31.0',
        'rsa>=4.9',
        'six>=1.16.0',
        'tzdata>=2023.3',
        'urllib3<=2.0',
        'watchdog>=3.0.0',
        'Werkzeug>=2.3.4'
    ],
    entry_points={
        'console_scripts': [
            'switchboard-cli=switchboard_py.cli:main',
        ],
    }
)
#to build project directory, in terminal run `switchboard-cli start_project <project_name> <cloud_provider>`