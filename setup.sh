#!/bin/bash

sudo apt-get update
sudo apt-get install -y python3
sudo apt-get install -y python3-pip
sudo apt-get install -y python-is-python3
pip3 install -U -r requirements.txt
