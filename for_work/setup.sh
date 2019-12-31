#!/usr/bin/bash

sudo apt-get install -y mysql-server
sudo apt-get install -y python3-pip

pip3 install pybufrkit

sudo apt-get install -y python-dev default-libmysqlclient-dev #for mysqlclient
sudo apt-get install -y build-essential libssl-dev libffi-dev python-dev #for mysqlclient

pip3 install mysqlclient


sudo mysql < tsaoscript.sql

python3 ../in_table_MYSQL_UGMS_and_Stations.py

echo software installed and tested congratulations
