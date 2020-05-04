import calendar,datetime,MySQLdb,os


with open('../for_work/index.txt', 'r') as f:
    r = f.read()

rr = [i.split() for i in r.split('\n') if i]
# словарь индексы - название станции
index_name_dict = {station[0]:station[1] for station in rr}

# словарь УГМС - список индексво
ugms_list = list(set([i[-1] for i in rr if len(i) == 3]))
ugms_dict = {i:[] for i in ugms_list}
for i in rr:
    if len(i) == 3:
        ugms_dict[i[-1]].append(i[0])

 # получаем количество дней в текущем месяце
now = datetime.datetime.now()
len_month = calendar.monthrange(now.year, now.month)[1]
month_now = now.month

# подключаемся к базе получаем список данных за сроки 00 и 12 
conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'cao_bufr_v2', charset="utf8")
cursor = conn.cursor()
cursor.execute(f'''select Stations_numberStation,  time_srok from cao_bufr_v2.releaseZonde where year(time_srok)={now.year} and month(time_srok)={month_now} and hour(time_srok)=00 order by day(time_srok);''')
data_month_00 = cursor.fetchall()
cursor.execute(f'''select Stations_numberStation,  time_srok from cao_bufr_v2.releaseZonde where year(time_srok)={now.year} and month(time_srok)={month_now} and hour(time_srok)=12 order by day(time_srok);''')
data_month_12 = cursor.fetchall()

# делаем два словаря индекс станции - список дней когда был выпуск
index_date_00_dict = {i:[] for i in index_name_dict.keys()}
index_date_12_dict = {i:[] for i in index_name_dict.keys()}
[index_date_00_dict[index_day[0]].append(index_day[1].day) for index_day in data_month_00 if index_day[0] in index_name_dict]
[index_date_12_dict[index_day[0]].append(index_day[1].day) for index_day in data_month_12 if index_day[0] in index_name_dict]

# срок|01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|
string_count_day_month = ''.join([f'{i:02d}|' for i in range(1,len_month + 1)])
first_string_table = f' срок|{string_count_day_month}'

sum_month = 0
# проходим по словарю угмс
table = 'Данные о выпусках\n'
for ugms,indexs in sorted(ugms_dict.items()):
    table += f'{ugms}\n{" ":21}{first_string_table}\n'
    # проходим по списку станций в угмс
    for index in sorted(indexs):
    # пишем данные о сроках 00
        string_time_00 = ''.join(["__|" if day in index_date_00_dict[index] else " N|" for day in range(1,len_month+1)])
        table += f'{index_name_dict[index]:>21} 00: |{string_time_00} всего {len(index_date_00_dict[index])}\n'
        # записываем данные о сроках 12
        string_time_12 = ''.join(["__|" if day in index_date_12_dict[index] else " N|" for day in range(1,len_month+1)])
        table += f'{index}{" ":17}12: |{string_time_12} всего {len(index_date_12_dict[index])}\n'
    # считаем суммы выпусков за месяц
    sum_00 = sum([len(index_date_00_dict[index]) for index in indexs])
    sum_12 = sum([len(index_date_12_dict[index]) for index in indexs])
    all_sum = sum_00 + sum_12
    sum_month += all_sum
    table += f'{" ":21}По УГМС всего:{all_sum}\n'
table += f'По УГМС за месяц {sum_month}'


dir_list = os.listdir('/home/bufr/reports')
dir_month_now = f'report_{month_now:02d}{now.year}'
if dir_month_now not in dir_list:
    os.mkdir(f'/home/bufr/reports/{dir_month_now}')

with open(f'/home/bufr/reports/{dir_month_now}/выпуски_зондов_{now.year}-{now.month}.nill', 'w') as f:
    f.write(table)
