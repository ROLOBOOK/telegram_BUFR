import MySQLdb, datetime
name = input('year month day hour: ')
year, month, day,hour = name.split()

conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'test', charset="utf8")

cursor = conn.cursor()
cursor.execute(f''' select Stations_numberStation, time_pusk, oborudovanie, text_info_ValueData_205060 from test.releaseZonde
where year(time_srok) = {year} and month(time_srok) = {month} and day(time_srok) = {day} and hour(time_srok) = {hour}
order by Stations_numberStation;''')

data_month = cursor.fetchall()

if data_month:
    result = ''.join([f'{i[1]} {i[0]} {i[2]} {i[3]}\n' for i in data_month]).replace('None', '-          ')
    with open(f'{year}-{month}-{day}_{hour}:00.txt', 'w') as f:
        f.write(result)
    print(f'report file  {year}-{month}-{day} {hour}:00')
else:
    print('base do not have data')
