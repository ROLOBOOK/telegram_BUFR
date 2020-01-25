#!/usr/bin/bash

# устанавливаем mysql сервер 5, pip3 для питона 7, ssh  для доступа с коносли 11, samba сделать сетевую папку 9,
# ставим библиотеки для обработки BUFR 14 и библиотеку для работы с базой mysql 20  

apt-get install -y mysql-server python3-pip samba ssh python-dev default-libmysqlclient-dev build-essential libssl-dev libffi-dev python-dev > log.txt

echo 'app was installing'

pip3 install pybufrkit >>log.txt

pip3 install mysqlclient >>log.txt

echo 'library was installing'

#  запускаем скрипт создания баз для хранения расшифрованых телеграмм

mysql < tsaoscript.sql

echo 'basa tsao was creating'

# записываем в базу информацию о станциях и УГМС
cd .. 
python3 ./add_new_station_in_base.py

echo 'Station in base'

# делаем папку folder_with_telegram сетевой, даем на нее права
cd ./folder_with_telegram
pwd=$(pwd)
sudo chmod -R 7777 $pwd
sudo chown -R nobody:nogroup $pwd

echo "[folder_with_telegram]
path = $pwd
browsable = yes
writable = yes
qest ok = yes
public = yes
read only = no" >> /etc/samba/smb.conf

echo 'share was creating'


echo FINISH
