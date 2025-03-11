# Ann Sibylle

Experimental setup for reliably recreating System configurations


## Requirements
 - Mainly a repository to recreate the status of my basement server setup

## Disaster Recovery
While this is aimed at beeing the guide for restoring the server setup from an offsite backup this will also be a step by step guide for how to recover the server in case of catastrophic failure.
Writing this now with a cool mind instead of having to figure things out when actual shit hits the fan

1. Obtain a new computer running ubuntu to be the target for the backup restoration
2. ???
3. Profit?

### Random List of comand i use to run this so i dont forget while im working this out:
Run the first_playbook.yml and pass the inventory:
`ansible-playbook --check first_playbook.yml -i inventory.ini`
`ansible-galaxy role install mailcow.mailcow``
While the PR: https://github.com/mailcow/mailcow-ansiblerole/pull/56 is still open this will not be possible to install from just the public galaxy. Instead use this version.
`ansible-galaxy role install git+https://github.com/JBDCE/mailcow-ansiblerole.git,master,mailcow-ansiblerole`
