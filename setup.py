from setuptools import setup, find_packages

setup(
    name='cloud-switchboard',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'google-cloud-storage>=2.9.0',
        'functions-framework>=3.0'
    ],
    entry_points={
        'console_scripts': [
            'switchboard-cli=switchboard_py.cli:main',
        ],
    }
)
#to build project directory, in terminal run `switchboard-cli start_project <project_name> <cloud_provider>`



