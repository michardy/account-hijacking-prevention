#! /bin/bash
#Script to setup server

sudo apt-get update
sudo apt-get install python-virtualenv
sudo apt-get install mongodb
sudo apt-get install nginx
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev #unbreak cryptography module
virtualenv venv -p python3
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
