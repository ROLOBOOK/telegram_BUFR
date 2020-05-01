import MySQLdb, os
from datetime import date, timedelta


data = []
yesterday = date.today() - timedelta(days=1)
year, month, day = yesterday.strftime('%Y.%m.%d').split('.') 
hour = '00'
conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'cao_bufr_v2', charset="utf8")
cursor = conn.cursor()
cursor.execute(f''' select Stations_numberStation, time_pusk, oborudovanie, text_info_ValueData_205060 from cao_bufr_v2.releaseZonde
where year(time_srok) = {year} and month(time_srok) = {month} and day(time_srok) = {day} order by Stations_numberStation;''')
data_month = cursor.fetchall()
data.extend(data_month)
hour='12'
cursor.execute(f''' select Stations_numberStation, time_pusk, oborudovanie, text_info_ValueData_205060 from cao_bufr_v2.releaseZonde
where year(time_srok) = {year} and month(time_srok) = {month} and day(time_srok) = {day} and hour(time_srok) = {hour}
order by Stations_numberStation;''')
data_month = cursor.fetchall()
data.extend(data_month)

if data:
    os.chdir('../../report_bufr_day')
    result = ''.join([f'{i[1]} {i[0]} {i[2]} {i[3]}\n' for i in data]).replace('None', '-          ')

    with open(f'{year}-{month}-{day}_00:00-12:00.txt', 'w') as f:
        f.write(result)
    print(f'report file  {year}-{month}-{day} {hour}:00')
else:
    print('base do not have data')
