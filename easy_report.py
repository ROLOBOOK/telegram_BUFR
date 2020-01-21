import MySQLdb, datetime
name = input('year month day hour: ')
year, month, day,hour = name.split()
try:

    conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'tsao', charset="utf8")

    cursor = conn.cursor()
    cursor.execute(f''' select Stations_numberStation, date_start, oborudovanie_zond, text_info from tsao.releaseZonde
    where year(date) = {year} and month(date) = {month} and day(date) = {day} and hour(date) = {hour}
    order by Stations_numberStation;''')

    data_month = cursor.fetchall()
except Exception as ex:

    print(ex)
result = ''.join([f'{i[0]} {i[1]} {i[2]} {i[3]}\n' for i in data_month])
with open(f'{year}-{month}-{day} {hour}:00:00', 'a') as f:
    f.write(result)
