# !/usr/bin/env python3

import os, MySQLdb
try:
    
    with open('telegram_BUFR/for_work/индексы.txt', 'r') as f:
                    indexs = {line.split()[0]: line.split()[-1].split('|') for line in f}
except:
    print('ошибка, данные из файла индексы.txt не получены')
    
data = set([i[-1] for i in indexs.values()])
data = [(i,) for i  in data]

 
# заполняем таблицу УГМС
try:
    conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'tsao', charset="utf8")
    cursor = conn.cursor()
# запись данных в таблицу    
    cursor.executemany('INSERT INTO tsao.UGMS (UGMS) VALUES (%s)',data)
    conn.commit()

    cursor.execute("SELECT * FROM tsao.UGMS")

except Exception as ex:
    print(f'ошибка при заполнении таблицы UGMS: {ex}')

# Разрываем подключение.
finally:
    conn.close()
    
    
# заполняем таблицу станции - индекс, название, id_УГМС

stations = [(i, indexs[i][0],ugms[indexs[i][1]]) for i in indexs ]
try:
    conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'tsao', charset="utf8")
    cursor = conn.cursor()
    
    cursor.executemany('INSERT INTO tsao.Stations VALUES (%s,%s,%s)',stations)
    conn.commit()

except Exception as ex:
    print(f'ошибка при заполнении таблицы Stations: {ex}')
    
# Разрываем подключение.
finally:
    conn.close()