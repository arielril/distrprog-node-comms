#!/bin/bash

echo 'Here is the boot guy!'

# Add aliases
echo 'alias la="ls -lah"' >/root/.bashrc 2>/dev/null
echo 'alias la="ls -lah"' >/home/vagrant/.bashrc 2>/dev/null

# Install necessary packages
sudo apt-get update &&
  sudo apt-get install -y \
    python3 \
    python3-venv

# Install wireshark enabled for non-root users
DEBIAN_FRONTEND=noninteractive apt -y install wireshark
debconf-set-selections <<<"wireshark-common wireshark-common/install-setuid boolean true"
DEBIAN_FRONTEND=noninteractive dpkg-reconfigure wireshark-common
usermod -a -G wireshark vagrant

# link python to python3
sudo ln -sf $(which python3) /bin/python

# install python deps
cd /home/vagrant/code/

python -m venv env
source env/bin/activate
pip install -r requirements.txt
cd /
