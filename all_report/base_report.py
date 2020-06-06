import calendar,datetime,MySQLdb,os,sys


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

# делаем два словаря будем заносить данные из базы
index_date_00_dict = {i:[] for i in index_name_dict.keys()}
index_date_12_dict = {i:[] for i in index_name_dict.keys()}


 # получаем  текущую дату и количество дней в текущем месяце
now = datetime.datetime.now()
len_month = calendar.monthrange(now.year, now.month)[1]
month_now = now.month
year_now = now.year

if len(sys.argv) == 2 and sys.argv[1].isdigit():
    now = sys.argv[1]
    y = int(now[:4])
    m = int(now[4:6])
    now = datetime.datetime(y, m, 28)
    len_month = calendar.monthrange(now.year, now.month)[1]
    month_now = now.month
    year_now = now.year



def work_with_dict(list_):
#'''записываем в словарь даные {индекс_cтанции: {день : данные}} '''
    index_date_dict = {i:{day:'' for day in range(1,month_now + 1)} for i in index_name_dict.keys()}
    list_ = [(i[0],i[1],int(i[2])) if i[2].isdigit() else (i[0],i[1],0) for i in list_]
    for index_day_dicriptor in sorted(list_, key=lambda x: (x[0],x[2])):
        if index_date_dict.get(index_day_dicriptor[0],0):
            index_date_dict[index_day_dicriptor[0]][index_day_dicriptor[1].day] = index_day_dicriptor[2]
    return index_date_dict


def load_data_from_bd(decriptor_2,decriptor='time_srok', month_now=month_now ,year_now=year_now, table_db='releaseZonde', point=', '):
    # подключаемся к базе получаем список данных за сроки 00 и 12
    conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'cao_bufr_v2', charset="utf8")
    cursor = conn.cursor()
    cursor.execute(f'''select Stations_numberStation,  {decriptor}{point}{decriptor_2} from cao_bufr_v2.{table_db} where year(time_srok)={year_now} and month(time_srok)={month_now} and hour(time_srok)=00 order by day(time_srok);''')
    data_month_00 = cursor.fetchall()
    cursor.execute(f'''select Stations_numberStation,  {decriptor}{point}{decriptor_2} from cao_bufr_v2.{table_db} where year(time_srok)={year_now} and month(time_srok)={month_now} and hour(time_srok)=12 order by day(time_srok);''')
    data_month_12 = cursor.fetchall()
    conn.close()
    return data_month_00, data_month_12



def save_report(table,now=now,file_name='txt',month_now=month_now):
    #  проверяем есть ли папка с именем текущего месяца, делаем если нет и записываем переданый файл
    dir_list = os.listdir('/home/bufr/reports')
    dir_month_now = f'report_{month_now:02d}{now.year}'
    if dir_month_now not in dir_list:
        os.mkdir(f'/home/bufr/reports/{dir_month_now}')

    with open(f'/home/bufr/reports/{dir_month_now}/{now.year}{now.month:02d}.{file_name}', 'w') as f:
        f.write(table)
