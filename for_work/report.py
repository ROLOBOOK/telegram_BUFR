import MySQLdb, datetime, conect_bd

name = input('year month day hour: ')
year, month, day,hour = name.split()

try:
    conn = MySQLdb.connect(conect_bd.server, conect_bd.username,\
                               conect_bd.password, conect_bd.bd, charset="utf8")
    cursor = conn.cursor()
    cursor.execute(f''' select index_station, time_pusk,\
           oborudovanie, text_info from cao2.info_pusk
           where year(time_srok) = {year} and month(time_srok) = {month} and \
           day(time_srok) = {day} and hour(time_srok) = {hour}
           order by index_station;''')
    data_month = cursor.fetchall()

except Exception as ex:
    print(ex)

if data_month:
    result = ''.join([f'{i[1]} {i[0]} {i[2]} {i[3]}\n' for i in data_month])
    with open(f'report_on_{year}-{month}-{day} {hour}:00.txt', 'a') as f:
        f.write(result)
    print(f'report file  on {year}-{month}-{day} {hour}:00')
else:
    print('base do not have data')
