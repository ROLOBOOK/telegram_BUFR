import os, MySQLdb 


def get_from_table(VALUES, table):
    try:
        conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'tsao', charset="utf8")
        cursor = conn.cursor()
        cursor.execute(f"SELECT {VALUES} FROM {table}")
    # # Получаем данные.
        data = cursor.fetchall()
    except Exception as ex:
        print(ex)
    # Разрываем подключение.
    finally:
        conn.close()
    return data
def set_in_table(table, VALUES, stations):
    try:
        conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'tsao', charset="utf8")
        cursor = conn.cursor()
        cursor.executemany(f'INSERT INTO {table} VALUES ({VALUES})',stations)
        conn.commit()
    except Exception as ex:
        print(f'ошибка при заполнении таблицы {table}: {ex}')
        return 0
    # Разрываем подключение.
    finally:
        conn.close()
    return 1
        
#получаем список индексов станций из базы
indexs_stations = [str(i[0]) for i in get_from_table('numberStation', 'tsao.Stations')]
#получаем список УГМС из базы
list_ugms = [str(i[0]) for i in get_from_table('UGMS','tsao.UGMS')] 
try:
    with open('for_work/index_Station_UGMS.txt', 'r') as f:
                    indexs = {line.split()[0]: line.split()[-1].split('|') for line in f} 
except:
    print('ошибка, данные из файла индексы.txt не получены') 
data = set([i[-1] for i in indexs.values()]) 
list_new_ugms = [(i,) for i in data if str(i) not in list_ugms] 
if list_new_ugms:
    set_in_table('tsao.UGMS (UGMS)', '%s', list_new_ugms)
    print('Новые УГМС записаны') 
else:
    print('Новых УГМС нет')
    
    
#получаем список УГМС из базы
ugms = {i[1]:i[0] for i in get_from_table('*','tsao.UGMS')}
    
stations = [(i, indexs[i][0],ugms[indexs[i][1]]) for i in indexs if str(i) not in indexs_stations] 
if stations:
    set_in_table('tsao.Stations', '%s,%s,%s', stations)
    print('Новые станции записаны') 
else:
    print('Нет новых Станций')
