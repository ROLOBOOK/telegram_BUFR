#!/usr/bin/bash

# устанавливаем mysql сервер 5, pip3 для питона 7, ssh  для доступа с коносли 11,
# ставим библиотеки для обработки BUFR 14 и библиотеку для работы с базой mysql 20  

apt-get install -y mysql-server python3-pip python-dev default-libmysqlclient-dev build-essential libssl-dev libffi-dev python-dev > log.txt

echo 'app was installing'

pip3 install pybufrkit >>log_install.txt
pip3 install Progress >> log_install.txt
pip3 install mysqlclient >>log_install.txt
pip3 install paramiko
echo 'library was installing'

#  запускаем скрипт создания баз для хранения расшифрованых телеграмм

mysql < cao_bufr_v2.sql && echo 'basa cao was creating'


echo FINISH
