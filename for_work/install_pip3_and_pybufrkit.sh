#!/usr/bin/bash

sudo apt-get install -y mysql-server
sudo apt-get install -y python3-pip
sudo apt-get install -y python-dev default-libmysqlclient-dev #for mysqlclient
pip3 install pybufrkit
pip3 install mysqlclient
