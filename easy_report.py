import MySQLdb, datetime
name = input('year month day hour: ')
year, month, day,hour = name.split()
try:

    conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'cao', charset="utf8")

    cursor = conn.cursor()
    cursor.execute(f''' select Stations_numberStation, date_start, oborudovanie_zond, text_info, prichina from cao.releaseZonde
    where year(date) = {year} and month(date) = {month} and day(date) = {day} and hour(date) = {hour}
    order by Stations_numberStation;''')

    data_month = cursor.fetchall()
except Exception as ex:

    print(ex)

if data_month:
    result = ''.join([f'{i[1]} {i[0]} {i[2]} {i[3]} {i[4]}\n' for i in data_month]).replace('None', '-          ')
    with open(f'{year}-{month}-{day}_{hour}:00.txt', 'w') as f:
        f.write(result)
    print(f'report file  {year}-{month}-{day} {hour}:00')
else:
    print('base do not have data')
