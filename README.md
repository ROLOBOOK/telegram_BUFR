# telegram_BUFR
обработка аэрологический телеграмм


установка
в папке for_work запустить (для запуска в терминале пишем bash  имя файла):
 1. файл install_pip3_and_pybufrkit.sh. Мы устанавливаем: mysql-server, pip3, библиотеки: pybufrkit, mysqlclient
 2. файл script_create_base_and_user.sh - создаем базу и пользователя

Работа с телеграммами

запускать скрипты из папки telegram_BUFR (для запуска пишем python3 имя файла):

in_table_MYSQL_UGMS_and_Stations.py записывает в базу информацию о станциях и УГМС берет из файла for_work/index_Station_UGMS.txt

телеграмы скопировать в папку folder_with_telegram

in_table_MYSQL_releaseZonde_and_contentTelegram.py декодирует телеграммы из папки folder_with_telegram, заносит данные наблюдений и инфомацию о выпуске в базу. Првереные файлы перемещает в папку folder_with_telegram/check_telegram

report_by_month.py - скрипт для составлении отчет за месяц о типах использованых радиозондах. При запуске запрашивает год и месяц за который требуется состваить отчет. После работы скрипта в папке telegram_BUFR будет сформирован текстовый файл отчет_по_радиозондам_за_год_месяц.txt
