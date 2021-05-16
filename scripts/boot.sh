#!/bin/bash

echo 'Here is the boot guy!'

# Add aliases
echo 'alias la="ls -lah"' >/root/.bashrc 2>/dev/null
echo 'alias la="ls -lah"' >/home/vagrant/.bashrc 2>/dev/null

# Install necessary packages
sudo apt-get update &&
  sudo apt-get install -y \
    python3

# link python to python3
sudo ls -s /bin/python $(which python3)

# install python deps
cd /home/vagrant/code/python

python -m venv env
source env/bin/activate
pip install -r requirements.txt

cd /
