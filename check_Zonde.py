from pybufrkit.renderer import FlatJsonRenderer
from pybufrkit.decoder import Decoder
import os, time, pickle

begin_time = time.time()
# индексы  имена станций и угмс
if not os.path.isfile('for_work/date_ugms.pkl'):
    try:
        if not os.path.isfile('for_work/index.pkl'):
            with open('for_work/индексы.txt', 'r') as f:
                indexs = {line.split()[0]: line.split()[-1].split('|') for line in f}
        else:
            with open('for_work/indexs.pkl','rb') as f:
                indexs = pickle.load(f)
        # тут будут данные о радиозондах        
        ugms = {indexs[key][-1]: {} for key in indexs} # {'Башкирское': {'28722': {}}
        s = {'00':'', '12':''}

        for station in indexs:
            ugms[indexs[station][-1]][station]={i: s.copy() for i in range(1,32)}
    except:
        print("ошибка чтения индексов станиций")
else:
    with open('for_work/date_ugms.pkl', 'rb') as f:
        ugms = pickle.load(f)
        
    with open('for_work/indexs.pkl', 'rb') as f:
        indexs = pickle.load(f)

# получаем файлы из папки "./" и список проверненых файлов из файла ckeking_fails
try:
    files = os.listdir(path="./")
    if not os.path.isfile('for_work/ckeking_fails'):
        f = open('for_work/ckeking_fails', 'a')
        f.close()
    with open('for_work/ckeking_fails', 'r') as c:
        if os.stat("for_work/ckeking_fails").st_size != 0:
            files_were_check_for_mistakes = c.read().split(';')
        else:
            files_were_check_for_mistakes = []
    files = [file for file in files if file[-3:] == 'bin' and file[:5] in indexs]
    file_with_mistake = []
except:
    print("ошибка получения списков файлов для расшифровки")


#поиск типов радиозондов, вывод в файл

for file_name in files:
#     провряем был ли раньше проверен этот файл, если да пропускаем итерацию если нет заносим его в базу
    if file_name in files_were_check_for_mistakes:
        continue
    files_were_check_for_mistakes.append(file_name)
#     выводи сколько проверно файлов и прошло времени
    if len(files_were_check_for_mistakes) % 10 == 0:
        end_time = int(time.time() - begin_time)
        print('проверено файлов: {}, за {:02d}:{:02d}:{:02d}'.format(len(files_were_check_for_mistakes),end_time%3600,end_time%600,end_time%60))
        

# декодируем burf в юникод
    try:
        decoder = Decoder()
        with open(f'07/{file_name}', 'rb') as ins: #
            bufr_message = decoder.process(ins.read())
        json_data = FlatJsonRenderer().render(bufr_message)
    except:
        print(f'{file_name} не декодирован')
        file_with_mistake.append((f'{file_name}, не декодирован'))
        continue

# записываем в словарь информацию о радиозонде из телеграммы 
    try:
        day_telegram = json_data[1][-4]
        time_telegram = '{:02d}'.format(json_data[1][-3])
        oborudovanie = json_data[3][2][0][30]
        zond = json_data[3][2][0][-1].decode('utf-8').split()[-1] if type(json_data[3][2][0][-1]) == bytes else '-'
        oborudovanie_zond = f'{oborudovanie} {zond}'
        index_station = '{}{:03d}'.format(json_data[3][2][0][27],json_data[3][2][0][28])
        ugms_stantion = indexs.get(index_station, index_station)[-1]
        ugms[ugms_stantion][index_station][day_telegram][time_telegram]=oborudovanie_zond
    except:
        print(f'ошибка в файле {file_name}, значение оборудования не занесено в базу')
        file_with_mistake.append((f'{file_name}, оборудования не занесено в базу'))
    
    with open('for_work/ckeking_fails', 'a') as c:
        c.write(';'.join(files_were_check_for_mistakes))

# записываем базу в файл date_ugms и indexs, файлы обработаные с ошибками для дальнейшего использования
with open('for_work/date_ugms.pkl', 'wb') as f:
    pickle.dump(ugms, f)
    
with open('for_work/indexs.pkl', 'wb') as f:
    pickle.dump(indexs,f)

with open('for_work/file_with_mistake','a') as f:
    f.write(';'.join(file_with_mistake))
    
# with open('for_work/ckeking_fails.pkl', 'wb') as f:
#     pickle.dump(files_were_check_for_mistakes, f)
    
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

with open('отчет_по_радиозондам_месяц.txt', 'a') as f:
    for ugms_stantion in ugms:
        f.write(f'{ugms_stantion}\n{string}\n')
        for index_station in ugms[ugms_stantion]:
            night = '{:<12} 00 |'.format(indexs[index_station][0][:12])
            moning ='{:<12} 12 |'.format(index_station)
            for day in ugms[ugms_stantion][index_station]:
                to00 = ugms[ugms_stantion][index_station][day].get('00', '-')
                if not to00: to00 = '-'
                night += '{:^9}|'.format(to00)
                to12 = ugms[ugms_stantion][index_station][day].get('12', '-')
                if not to12: to12 = '-'
                moning +='{:^9}|'.format(to12)
            f.write(f'{night}\n{moning}\n')
            # впишем в файл сумму значений типов зондов по станции
            s = ''
            for i in sum_zonde_station[index_station]:
                z = 'No' if not i[0] else i[0]
                s += f'{z} = {i[-1]}; '
            f.write(f'По станции {indexs[index_station][0]} всего: {s[:-2]}\n\n')
         # впишем в файл сумму значений типов зондов по УГМС
        s = ''
        for i in sum_zonde_ugms[ugms_stantion]:
            z = 'No' if not i[0] else i[0]
            s += f'{z} = {i[-1]}; '
        f.write(f'По УГМС {ugms_stantion} всего: {s[:-2]}\n\n')
        


end_time = int(time.time() - begin_time)
print('проверено файлов: {}, за {:02d}:{:02d}:{:02d}'.format(len(files_were_check_for_mistakes),end_time%3600,end_time%600,end_time%60))

