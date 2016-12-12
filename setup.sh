#! /bin/bash

sudo apt-get install python-virtualenv
sudo apt-get install mongodb
virtualenv venv
source venv/bin/activate -p python3
pip install --upgrade pip
pip install requirements.txt
