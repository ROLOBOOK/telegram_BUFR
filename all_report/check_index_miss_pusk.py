import MySQLdb,re, datetime, sys, os
sys.path.insert(1, '../')
from for_work.email import send_email

def get_str_list_station_RF():
    with open('../for_work/index.txt') as f:
        s = f.read()
    index_name = {i.split()[0]:i.split()[1:] for i in s.split('\n') if i}
    return ','.join(re.findall(r'\d{5}',s)), index_name 

def get_meta_info_for_srock(str_list_station_RF,year,month,day,table='releaseZonde'):
     try:
         conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'cao_bufr_v2', charset="utf8")
         cursor = conn.cursor()
         cursor.execute(f'''select Stations_numberStation,time_srok from cao_bufr_v2.{table}
         where year(time_srok)={year} and month(time_srok)={month} and day(time_srok)={day} and hour(time_srok)=12
 and Stations_numberStation in ({str_list_station_RF})''')
         from_bd_metainfo_yesterday_12 = set([f'{index[0]} - {index[1]}' for index in cursor.fetchall() if index])
         day = f'{int(day)+1:02}'
         cursor.execute(f'''select Stations_numberStation,time_srok from cao_bufr_v2.{table}
         where year(time_srok)={year} and month(time_srok)={month} and day(time_srok)={day} and hour(time_srok)=0
 and Stations_numberStation in ({str_list_station_RF})''')
         from_bd_metainfo_now_00 = set([f'{index[0]} - {index[1]}' for index in cursor.fetchall() if index])

     except:
         from_bd_metainfo_yesterday_12 = 'ERROR GET INFO FROM BD'
         from_bd_metainfo_now_00 = ''
     finally:
         conn.close()
     return from_bd_metainfo_yesterday_12, from_bd_metainfo_now_00

def get_miss_two_part_telegamm():
    pass



if __name__ == '__main__':
    str_list_station_RF,index_name = get_str_list_station_RF()
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1) 
    year, month, day = yesterday.strftime('%Y.%m.%d').split('.')

    from_bd_metainfo_yesterday_12, from_bd_metainfo_now_00 = get_meta_info_for_srock(str_list_station_RF,year,month,day)

    from_bd_metainfo = from_bd_metainfo_yesterday_12.union(from_bd_metainfo_now_00)



    from_bd_last_h_yesterday_12,from_bd_last_h_now_00 = get_meta_info_for_srock(str_list_station_RF,year,month,day, table='last_H')
    from_bd_last_h =  from_bd_last_h_yesterday_12.union(from_bd_last_h_now_00)

    filename = '/home/bufr/bufr_work/telegram_BUFR/temp_check_files_get_index.txt' 
    if os.path.isfile(filename):
        with open(filename) as f:
            must_to_be_bd = set([i.strip() for i in f.read().split('#'*50)[-1].split('\n') if i and i.split(' - ')[0] in str_list_station_RF.split(',')])
    input_but_not_bd = must_to_be_bd - from_bd_metainfo
    res_metinfo = '\n'.join(input_but_not_bd)

    get_bufr_from_stantion = [index.split(' - ')[0] for index in from_bd_metainfo if index]

    telegramma_get = []
    telegramma_not_get = []
    not_get_bufr_from_stantion = [telegramma_get.append(index) if index in get_bufr_from_stantion else telegramma_not_get.append(index) for index in str_list_station_RF.split(',')]


    res_last_h = '\n'.join(must_to_be_bd - from_bd_last_h)
    str_srok12 = f'{ yesterday.strftime("%d.%m.%Y")} 12:00'
    str_srok00 =  f'{int(day)+1:02}.{month}.{year} 00:00'
    telegramma_not_get_dict = {str_srok12:[], str_srok00:[]}
    srok_12 = [index.split(' - ')[0] for index in from_bd_metainfo_yesterday_12]
    srok_00 = [index.split(' - ')[0] for index in from_bd_metainfo_now_00]

    [telegramma_not_get_dict[str_srok12].append(index) for index in  telegramma_not_get if index not in srok_12]
    [telegramma_not_get_dict[str_srok00].append(index) for index in telegramma_not_get if index not in srok_00]


    res = f'За вчерашницй день\nВ таблицу с метаданными не поступили данные со станций:\n{res_metinfo if res_metinfo else "ошибок не найдено"}\n{"*"*40}\nВ таблицу последних высот не поступили данные со станций:\n{res_last_h if res_last_h else "ошибок не найдено"}\n'
    res += f'\nBUFR получены со станций:\n{", ".join(telegramma_get)}\n\nBUFR НЕ получены со станций:\nСрок {str_srok12}\n{", ".join(telegramma_not_get_dict[str_srok12])}\n\nСрок {str_srok00}\n{", ".join(telegramma_not_get_dict[str_srok00])}'

    print(res)
    send_email(body=res, subject='в базе нет данных от станций', file='send')
