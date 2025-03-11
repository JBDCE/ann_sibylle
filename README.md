# Ann Sibylle
Experimental setup for reliably recreating System configurations

## Requirements
 - Mainly a repository to recreate the status of my basement server setup

## Setup Instructions
To get started using this repository the following commands need to be executed after cloning this repository:
 - `sudo apt install python3 python3-venv`
 - `python3 -m venv venv`
 - `source venv/bin/activate`

You should by this point be inside a virtual environment and be able to start installing the requirements for this repository

 - `pip install -r python-requirements.txt`

This might take a while. The ansible installation might also not produce any log output during that

 - `ansible-galaxy install -r ansible-requirements.yml`

After this is done you should have all requirements installed to execute every playbook within this repository.
If this is actually used in a different environment the inventory.ini file will have to be updated according to the machines ip adresses.

## Including a new machine to be configured
When a new target is added to the inventory file the system running this ansible repo must have access to the new machine. Roll out the public key for the ansible host to the target.

A reminder to myself that [this](https://github.com/JBDCE/authorizedkeys) repo also exists:

## Disaster Recovery
While this is aimed at beeing the guide for restoring the server setup from an offsite backup this will also be a step by step guide for how to recover the server in case of catastrophic failure.
Writing this now with a cool mind instead of having to figure things out when actual shit hits the fan

1. Obtain a new computer running ubuntu to be the target for the backup restoration
2. ???
3. Profit?

### Random List of comand i use to run this so i dont forget while im working this out:
Run the first_playbook.yml and pass the inventory:
`ansible-playbook --check first_playbook.yml -i inventory.ini`
