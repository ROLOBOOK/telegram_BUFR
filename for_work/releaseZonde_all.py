import os, MySQLdb



def get_from_table(VALUES, table):
    try:
        conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'cao', charset="utf8")
        cursor = conn.cursor()
        cursor.execute(f''' select {VALUES} from {table} order by Stations_numberStation;''')

    # # Получаем данные.
        data = cursor.fetchall()

    except Exception as ex:
        print(ex)

    # Разрываем подключение.
    finally:
        conn.close()

    return data


all_releaseZonde = get_from_table('Stations_numberStation, date_start, oborudovanie_zond, text_info','cao.releaseZonde')


result = ''.join([f'{i[1]} {i[0]} {i[2]} {i[3]}\n' for i in all_releaseZonde])
if result:
    with open('all_in_table_resleaseZonde.txt', 'w') as f:
        f.write(result)
    print('file is ready')
else:
    print('table is empty')
