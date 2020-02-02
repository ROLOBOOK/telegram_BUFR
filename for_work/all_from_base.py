import os, MySQLdb, conect_bd



def get_from_table(VALUES, table):
    try:
        conn = MySQLdb.connect(conect_bd.server, conect_bd.username,\
                               conect_bd.password, conect_bd.bd, charset="utf8")
        cursor = conn.cursor()
        cursor.execute(f''' select {VALUES} from {table} order by index_station;''')

    # # Получаем данные.
        data = cursor.fetchall()

    except Exception as ex:
        print(ex)

    # Разрываем подключение.
    finally:
        conn.close()

    return data


all_releaseZonde = get_from_table("index_station, time_pusk,oborudovanie, text_info", 'cao2.info_pusk' )


result = ''.join([f'{i[1]} {i[0]} {i[2]} {i[3]}\n' for i in all_releaseZonde])
if result:
    with open('all_in_table_resleaseZonde.txt', 'w') as f:
        f.write(result)
    print('file is ready')
else:
    print('table is empty')
