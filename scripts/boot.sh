#!/bin/bash

echo 'Here is the boot guy!'

# Install necessary packages
sudo apt-get update \
  && sudo apt-get install -y \
    default-jdk

# Add aliases
echo 'alias la="ls -lah"' > /root/.bashrc 2>/dev/null
echo 'alias la="ls -lah"' > /home/vagrant/.bashrc 2>/dev/null
