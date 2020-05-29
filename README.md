# pulumi-azure-testing
This is run on fedora 31 with python as runtime language for pulumi.  
The documentation is kept as simple as possible and the project will probably not be further extended in this repository.  

## Requirements

This is in part copied from the official pulumi website: https://www.pulumi.com/docs/get-started/azure/begin/ 

Install Pullumi CLI

```bash
$ curl -fsSL https://get.pulumi.com | sh
$ pulumi version 
# v2.3.0
```

Verify that active python version is >=3.6

```bash
$ python --version 
# eg. Python 3.7.7
```

Verify that Azure CLI 2.0 is installed

```bash
# install guide
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-yum?view=azure-cli-latest
$ az version 
# {
#   "azure-cli": "2.6.0",
#   ..... }
```

Other requirements: 
* Valid azure user with active subscription
* pulumi user account

## Start a project

A pulumi project needs to be started in an empty directory

```bash
$ mkdir my-new-dir
$ pulumi new azure-python 
```

The new project wizard will then ask the user to define some metadata considering azure. Check out the official guide for further information on this part.

Add a python virtual env for pulumi libraries (because installing everything locally is ugly :-) )

```bash
# virtualenvwrapper is used here
$ mkvirtualenv pulumi

# virtualenvwrapper automatically sources the newly created env

# install all needed libraries
$ pip install -r requirements.txt
```

Sign in to azure cloud with ```az login```

Have Fun! 

## Deploy some vms

The given example to deploy some vms using a python loop can be used as follows: 

```bash
$ cd deploy-vms

# initialize pulumi stack if not already
$ pulumi init

# verify that you are in a venv and have the needed pip libraries installed
$ pip install -r requirements.txt

# apply the definition
$ pulumi up
```

Pulumi will then parse the file and check what needs to be done on the azure cloud to fulfill the desired state. After an evaluation phase it asks the user, if the given ressources should be deployed as asked.  