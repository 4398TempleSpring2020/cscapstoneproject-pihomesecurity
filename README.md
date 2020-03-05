# cscapstoneproject-pihomesecurity

## Loading Dependencies
Prior to developing, install dependencies for the virtual environment and activate the environment. General instructions for working with virtualenv can be found in create_envs.txt at the root of the project architecture

To install any dependencies follow the instructions below:

1) construct a blank virtual environment with:
 virtualenv ./environments/pi_env

2) activate the virtual environment with:
 source ./environments/pi_env/bin/activate

3) install dependencies with:
 pip3 install -r requirements.txt --upgrade
 where the requirements file can be found within the environments folder.

## Saving Dependencies
Be sure to update the requirements file after installing any libraries. To update the file follow instructions below:

1) activate the virtual environment with:
 source ./environments/pi_env/bin/activate

2) save project dependencies:
 pip3 freeze --local > ./environments/requirements.txt