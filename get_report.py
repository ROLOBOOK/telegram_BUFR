import MySQLdb, os
from datetime import date, timedelta


data = []
yesterday = date.today() - timedelta(days=1)
year, month, day = yesterday.strftime('%Y.%m.%d').split('.') 
hour = '00'
conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'cao_bufr_v2', charset="utf8")
cursor = conn.cursor()
cursor.execute(f''' select Stations_numberStation, time_pusk, oborudovanie, text_info_ValueData_205060 from cao_bufr_v2.releaseZonde
where year(time_srok) = {year} and month(time_srok) = {month} and day(time_srok) = {day} and hour(time_srok) in ({hour},01)  order by Stations_numberStation;''')
data_month = cursor.fetchall()
data.extend(data_month)
hour='12'
cursor.execute(f''' select Stations_numberStation, time_pusk, oborudovanie, text_info_ValueData_205060 from cao_bufr_v2.releaseZonde
where year(time_srok) = {year} and month(time_srok) = {month} and day(time_srok) = {day} and hour(time_srok) in ({hour},13)
order by Stations_numberStation;''')
data_month = cursor.fetchall()
data.extend(data_month)

with open('for_work/index.txt', 'r') as f:
    r = f.read()
index_russian = [index.split()[0] for index in r.split('\n') if index]

data = [dat for dat in data if dat[0] in index_russian]

dir_list = os.listdir('/home/bufr/reports')
dir_month_now = f'report_{month}{year}'
if dir_month_now not in dir_list:
    os.mkdir(f'/home/bufr/reports/{dir_month_now}')

dir_list = os.listdir('/home/bufr/reports')
dir_month_now = f'report_{month}{year}'
if dir_month_now not in dir_list:
    os.mkdir(f'/home/bufr/reports/{dir_month_now}')

dir_list = os.listdir(f'/home/bufr/reports/{dir_month_now}')
if 'report_bufr_day' not in dir_list:
    os.mkdir(f'/home/bufr/reports/{dir_month_now}/report_bufr_day')

if data:
    os.chdir(f'/home/bufr/reports/{dir_month_now}/report_bufr_day')
    result = ''.join([f'{i[1]} {i[0]} {i[2]} {i[3]}\n' for i in data]).replace('None', '-          ')

    with open(f'{year}{month}{day}_0012.bdc', 'w') as f:
        f.write(result)
    #print(f'report file  {year}-{month}-{day} {hour}:00')
else:
    print('base do not have data')
