from base_report import *
from collections import Counter



def get_data_from_bd(table='releaseZonde', columns='Stations_numberStation', criterion='',month=month_now):
    conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'cao_bufr_v2', charset="utf8")
    cursor = conn.cursor()
    cursor.execute(f'''select {columns} from cao_bufr_v2.{table} {criterion};''')
    data = cursor.fetchall()
    conn.close()
    return data



count_pusk_month = get_data_from_bd(columns='Stations_numberStation, count(Stations_numberStation)',
                                    criterion=f'where month(time_srok)={month_now} group by Stations_numberStation')
#считаем среднюю высоту по станциям за месяц
avg_H_month = get_data_from_bd(columns='*', table='last_H',
                             criterion=f'where  h!="-" and month(time_srok)={month_now}')

s = {f'{i[0]};{i[1].strftime("%Y:%m:%d")}':int(i[-1]) for i in avg_H_month}
for value in avg_H_month:
    if int(value[-1]) > s[f'{value[0]};{value[1].strftime("%Y:%m:%d")}']:
	    s[f'{value[0]};{value[1].strftime("%Y:%m:%d")}'] = int(value[-1])

list_h_stations = [(i.split(';')[0],s[i]) for i in s]

dict_h = {v:[] for v in set([i[0] for i in list_h_stations])}

[dict_h[i[0]].append(i[1]) for i in list_h_stations]

avg_H_month = [(i,sum(dict_h[i])/len(dict_h[i])) for i in dict_h] 



count_type_zonde_month =get_data_from_bd(columns='Stations_numberStation, oborudovanie',
                                         criterion=f' where month(time_srok)={month_now}')

count_end_month = get_data_from_bd(columns='Stations_numberStation, descriptor_035035',
                                   criterion=f' where month(time_srok)={month_now}')
#считаем количество типов радиозондов
count_type_zonds = {i:[] for i in index_name_dict}
[count_type_zonds[i[0]].append(i[1][:3]) for i in count_type_zonde_month if i[0] in count_type_zonds]
counter_type = {i:Counter(count_type_zonds[i]) for i in count_type_zonds if count_type_zonds[i]}

#
count_end_pusk = {i:[] for i in index_name_dict}
[count_end_pusk[i[0]].append(i[1]) for i in count_end_month if i[0] in count_end_pusk]
counter_end = {i:Counter(count_end_pusk[i]) for i in count_end_pusk if count_end_pusk[i]}

#добавляем количество зондов и процент
dict_ = {i[0]:[i[1],round(i[1] / (len_month*2) * 100,2)] for i in  count_pusk_month if i[0] in index_name_dict}
#добавляем  среднюю высоту
[dict_[i[0]].append(int(i[1])) for i in avg_H_month if i[0] in index_name_dict]
#добавляем количество типов выпущеных зондов
[dict_[i].append(counter_type[i]) for i in dict_]
#добавляем  количесвто присины окончания
[dict_[i].append(counter_end[i]) for i in dict_]


if __name__ =='__main__':
    columns_name3 = f'|{" "*len("Станции/Управления")}| кол-во | %, плана |{"м":^12}| МРЗ-3АК | МРЗ-3МК | МРЗ-Н1 | АК2-2м | РЗМ-2| И-2012|"Ошибочный код"|"1"|"6"|"7"|"8"|"14"|"прочее"|'
    top = f'+{"-"*(len(columns_name3)-2)}+'

    columns_name1 = f'|{" "*len("Станции/Управления")}|{"Поступление":^19}|{"Высота":^12}|{"Количество выпущеный радиозондов по телеграммам BUFR":^68}|{"Кол-во выпусков,":^29}|'
    columns_name2 = f'|Станции/Управления|{"телеграмм в BUFR":19}|зондирования|{" ":68}|{"которые закончились":^29}|'
    columns_name4 = f'|{" "*len("Станции/Управления")}|{"-"*(len(columns_name3)-21)}|'

    table = f'{top}\n{columns_name1}\n{columns_name2}\n{columns_name4}\n{columns_name3}\n{top}\n'

    rf = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    for ugms,stations in sorted(ugms_dict.items()):
        ugms_sum = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
        for index in sorted(stations,key=lambda x:index_name_dict[x]):
            if index in dict_:
                mp3_pak = dict_[index][3].pop('058',0) + dict_[index][3].pop('089',0)
                mp3_3mk = dict_[index][3].pop('162',0)
                mp3_h1 = dict_[index][3].pop('119',0)
                ak2_2m = dict_[index][3].pop('090',0)
                p3m_2 = dict_[index][3].get('068',0) + dict_[index][3].pop('069',0)
                u_2012 = dict_[index][3].get('153',0) + dict_[index][3].pop('160',0)
                mistake_cod = sum(dict_[index][3].values())
                one = dict_[index][4].pop('1',0)
                six = dict_[index][4].pop('6',0)
                seven = dict_[index][4].pop('7',0)
                eight = dict_[index][4].pop('8',0)
                fortin = dict_[index][4].pop('14',0)
                other = sum(dict_[index][4].values())

                [ugms_sum[i].append(zond) for i,zond in enumerate((mp3_pak,mp3_3mk,mp3_h1,ak2_2m,p3m_2,u_2012,mistake_cod,one,six,seven,eight,fortin,other))]
                table += f'|{index_name_dict[index]:18}|{str(dict_[index][0]):^8}|{str(dict_[index][1]):^10}|{str(dict_[index][2]):^12}|{mp3_pak:^9}|{mp3_3mk:^9}|{mp3_h1:^8}|{ak2_2m:^8}|{p3m_2:^7}|{u_2012:^6}|{mistake_cod:^15}|{one:^3}|{six:^3}|{seven:^3}|{eight:^3}|{fortin:^4}|{other:^8}|\n'

            else:
                table += f'|{index_name_dict[index]:18}|{0:^8}|{0:^10}|{0:^12}|{0:^9}|{0:^9}|{0:^8}|{0:^8}|{0:^7}|{0:^6}|{0:^15}|{0:^3}|{0:^3}|{0:^3}|{0:^3}|{0:^4}|{0:^8}|\n'

        sum_h_ugms = sum([dict_[index][0] for index in stations if index in dict_])
        sum_plan = round(sum_h_ugms/(len_month*2*len(stations)) * 100,2)
        h =[dict_[index][2] for index in stations if index in dict_] 
        midl_h = str(sum(h)// len(h)) if len(h) else 0
        table += f'|{ugms[:15]:16}{len(stations):>2}|{str(sum_h_ugms):^8}|{sum_plan:^10}|{midl_h:^12}|{sum(ugms_sum[0]):^9}|{sum(ugms_sum[1]):^9}|{sum(ugms_sum[2]):^8}|{sum(ugms_sum[3]):^8}|{sum(ugms_sum[4]):^7}|{sum(ugms_sum[5]):^6}|{sum(ugms_sum[6]):^15}|{sum(ugms_sum[7]):^3}|{sum(ugms_sum[8]):^3}|{sum(ugms_sum[9]):^3}|{sum(ugms_sum[10]):^3}|{sum(ugms_sum[11]):^4}|{sum(ugms_sum[12]):^8}|\n{top}\n'


        all_in_list = [sum_h_ugms,sum_plan,midl_h] + [i[0] for i in ugms_sum if i]
        [rf[i].append(counts) for i,counts in enumerate(all_in_list)]

    all_stations = []
    for stations in ugms_dict.values():
        for  i in stations:
            all_stations.append(i)

    table += f'|{"По РФ":14} {len(all_stations):>3}|{sum(rf[0]):^8}|{round(sum(rf[0])/(len_month*2*len(all_stations)) * 100,2):^10}|{(sum([int(i) for i in rf[2]])//len(rf[2])):^12}|{sum(rf[3]):^9}|{sum(rf[4]):^9}|{sum(rf[5]):^8}|{sum(rf[6]):^8}|{sum(rf[7]):^7}|{sum(rf[8]):^6}|{sum(rf[9]):^15}|{sum(rf[10]):^3}|{sum(rf[11]):^3}|{sum(rf[12]):^3}|{sum(rf[13]):^3}|{sum(rf[14]):^4}|{sum(rf[15]):^8}|\n{top}\n'





    save_report(table, file_name='bstat',now=now,month_now=month_now)
