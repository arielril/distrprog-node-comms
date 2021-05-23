#!/bin/bash

echo 'Here is the alias guy!'

# Add aliases
echo 'alias la="ls -lah"' >/root/.bashrc 2>/dev/null
echo 'alias la="ls -lah"' >/home/vagrant/.bashrc 2>/dev/null

echo 'alias run-super1="make IP=192.168.35.10 PORT=5000 CONFIG=supernode1 GROUP_SIZE=2 r-super"' >/home/vagrant/.bashrc 2>/dev/null
echo 'alias run-super2="make IP=192.168.35.10 PORT=5001 GROUP_SIZE=2 CONFIG=supernode2 r-super"' >/home/vagrant/.bashrc 2>/dev/null
echo 'alias run-node1="make IP=192.168.35.11 PORT=8000 CONFIG=node1 r-node"' >/home/vagrant/.bashrc 2>/dev/null
echo 'alias run-node2="make IP=192.168.35.12 PORT=8000 CONFIG=node2 r-node"' >/home/vagrant/.bashrc 2>/dev/null
echo 'alias run-node3="make IP=192.168.35.12 PORT=8001 CONFIG=node3 r-node"' >/home/vagrant/.bashrc 2>/dev/null
