# отчет_по_радиозондам_за_месяц.txt
    
# ПОЛУЧАЕМ ДАННЫЕ ИЗ БАЗЫ
import MySQLdb

try:
    conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'tsao', charset="utf8")
    cursor = conn.cursor()
# # Получаем данные.

# releaseZonde ИНФА ПО ЗОНДАМ ЗА МЕСЯЦ ('Северное', 20046, '90 10310', 1, 0),
    cursor.execute('''SELECT u.Ugms, r.Stations_numberStation, r.oborudovanie_zond, day(r.date), hour(r.date)
    FROM tsao.releaseZonde as r left join tsao.Stations as s on r.Stations_numberStation = s.numberStation
    left join tsao.UGMS as u on u.idUGMS = s.UGMS_idUGMS
    order by Stations_numberStation, date;''')
    data_month = cursor.fetchall()
    
# СПИСОК УГМС   'Сев.-Кавказское',), 
    cursor.execute('''SELECT UGMS FROM tsao.UGMS''')
    data_UGMS = cursor.fetchall()
    
# СПИСОК (20046, 'Северное', 'Им.Э.Г.Кренкеля'),
    cursor.execute('''SELECT s.numberStation, u.UGMS, s.name_stations FROM tsao.Stations as s 
    left join tsao.UGMS as u on s.UGMS_idUGMS = u.idUGMS''')
    data_station_ugms = cursor.fetchall()
        
except Exception as ex:
    print(ex)
# Разрываем подключение.
finally:
    conn.close()

    
data_name_station = {i[0]:i[-1] for i in data_station_ugms}    # {20046: 'Им.Э.Г.Кренкеля',

ugms = {i[0]: {} for i in data_UGMS} #{'Башкирское': {}
s = {0:'', 12:''}
for i in data_station_ugms:
    ugms[i[1]][i[0]] = {i: s.copy() for i in range(1,32)} #  UGMS {'Башкирское': {28722: {1: {0: '', 12: ''},     


    
# ЗАНОСИМ В СЛОВАРЬ UGMS   data_month  
    
for data in data_month:
    ugms[data[0]][data[1]][data[3]][data[4]] = data[2]
    
# считаем количество типов радиозондов по станциям и по УГМС

station = {}
for ugms_stantion in ugms:
    for index_station in ugms[ugms_stantion]:
        station[index_station] = ugms[ugms_stantion][index_station]
        
sum_zonde_station = {}
sum_zonde_ugms = {}

# считаем сумму по станциям
a = {} # временный словарь
for key,value in station.items():
    a[key] = []
    for i in value.values():
        ([a[key].append(f) for f in i.values()])
    for k in a.values():
        sum_zonde_station[key] = [(name, k.count(name)) for name in set(k)]
    
        
# считаем сумму по УГМС
a = {} # временный словарь
for ugms_stantion in ugms:
    a[ugms_stantion] = []
    for index_station in ugms[ugms_stantion]:
        [a[ugms_stantion].append(f) for f in sum_zonde_station[index_station]]
    set_zonde = [i for i in set([n[0] for n in a[ugms_stantion]])]
    
    sum_zonde_ugms[ugms_stantion] = [(i, sum([n[1] for n in a[ugms_stantion] if n[0] == i])) for i in set_zonde]
sum_zonde_ugms    
    
            
# записываем в файл информацию о радиозонде из словаря                      
string = '{:>16}|'.format('срок')
for i in range(1,32):
    string += '{:^9}|'.format(i)

with open('отчет_по_радиозондам_за_месяц.txt', 'a') as f:
    
    for ugms_stantion in ugms:
        
        f.write(f'{ugms_stantion}\n{string}\n')
        
        for index_station in ugms[ugms_stantion]:
            
            night = '{:<12} 00 |'.format(data_name_station[index_station][:12])
            moning ='{:<12} 12 |'.format(index_station)
            
            for day in ugms[ugms_stantion][index_station]:
                to00 = ugms[ugms_stantion][index_station][day].get(0, '-')
                if not to00: to00 = '-'
                night += '{:^9}|'.format(to00)
                to12 = ugms[ugms_stantion][index_station][day].get(12, '-')
                if not to12: to12 = '-'
                moning +='{:^9}|'.format(to12)
            f.write(f'{night}\n{moning}\n')
            # впишем в файл сумму значений типов зондов по станции
            s = ''
            for i in sum_zonde_station[index_station]:
                z = 'No' if not i[0] else i[0]
                s += f'{z} = {i[-1]}; '
            f.write(f'По станции {data_name_station[index_station]} всего: {s[:-2]}\n\n')
# впишем в файл сумму значений типов зондов по УГМС
        s = ''
        for i in sum_zonde_ugms[ugms_stantion]:
            z = 'No' if not i[0] else i[0]
            s += f'{z} = {i[-1]}; '
        f.write(f'По УГМС {ugms_stantion} всего: {s[:-2]}\n\n')
        
