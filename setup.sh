#! /bin/bash

sudo apt-get install python-virtualenv
virtualenv venv
source venv/bin/activate -p python3
pip install --upgrade pip
pip install requirements.txt
