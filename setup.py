from setuptools import setup, find_packages

setup(
    name='cloud-switchboard',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'switchboard-cli=switchboard_py.cli:main',
        ],
    }
)
