# python-sample


# DEPENDENCIES

Version: Python 3

All depencendies are listed in requirements.txt.  To install use the following command.

### MacOS
It is recommended that local dependencies are installed using Python Virtual Environments.

````
python3 pip install virtualenv
python3 -m venv env
source ./env/bin/activate
python3 -m pip install -r requirements.txt
````

# DEV AND BUILD TOOLS

Python 3 is used as the main development and build tooling and can be used from a local installation with the start or watch scripts.  Remember to use Python Virtual environment for local development.

### Python Virtual environment
````
source ./env/bin/activate
````

### Start
````
./start.sh
````

### Testing
Testing script can be used 

````
python -m pytest
````

# WEB SERVER

