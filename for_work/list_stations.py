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


#получаем список индексов станций из базы
indexs_stations = [i[0] for i in get_from_table('numberStation', 'cao.Stations')]
#получаем список УГМС  из базы
list_ugms = [i[0] for i in get_from_table('UGMS','cao.UGMS')]

if indexs_stations:
    print(*indexs_stations, sep='     ')
    print()
    print(*list_ugms, sep='     ')
else: 
    print('empty')
