import os, MySQLdb 


def get_from_table(VALUES, table):
    try:
        conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'cao', charset="utf8")
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
        conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'cao', charset="utf8")
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
indexs_stations = [str(i[0]) for i in get_from_table('numberStation', 'cao.Stations')]
#получаем список УГМС из базы
list_ugms = [str(i[0]) for i in get_from_table('UGMS','cao.UGMS')] 

try:
    with open('for_work/index.txt', 'r') as f:
                    d = f.read()

    indexs = [i.split() for i in d.split('\n') if i]
    dict_ugms = {i[-1]:[] for i in indexs}
    for i in indexs:
        dict_ugms[i[-1]].append((i[0],i[1]))

except Exception as Ex:
    print(f'ошибка, данные из файла индексы.txt не получены\n{Ex}') 
 
list_new_ugms = [(i,) for i in list(dict_ugms.keys()) if str(i) not in list_ugms] 

if list_new_ugms:
    set_in_table('cao.UGMS (UGMS)', '%s', list_new_ugms)
    print('Новые УГМС записаны') 
else:
    print('Новых УГМС нет')
    
    
#получаем список УГМС из базы
ugms = {i[1]:i[0] for i in get_from_table('*','cao.UGMS')}
    

stations = [(i[0], i[1],ugms[i[-1]]) for i in indexs if str(i[0]) not in indexs_stations] 
if stations:
    set_in_table('cao.Stations', '%s,%s,%s', stations)
    print('Новые станции записаны') 
else:
    print('Нет новых Станций')
