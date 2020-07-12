from base_report import *

data_month_00, data_month_12 = load_data_from_bd('time_srok', point='', decriptor='', month_now=month_now)

# делаем два словаря индекс станции - список дней когда был выпуск
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
table += f'По УГМС за месяц {sum_month}\n'


# делаем два словаря для СНГ индекс станции - список дней когда был выпуск
[index_date_00_dict_cng[index_day[0]].append(index_day[1].day) for index_day in data_month_00 if index_day[0] in index_name_cng]
[index_date_12_dict_cng[index_day[0]].append(index_day[1].day) for index_day in data_month_12 if index_day[0] in index_name_cng]

sum_month_cng = 0

for ugms,indexs in sorted(ugm_cng.items()):
    table += f'{ugms}\n{" ":21}{first_string_table}\n'
    # проходим по списку станций в угмс
    for index in sorted(indexs):
    # пишем данные о сроках 00
        string_time_00 = ''.join(["__|" if day in index_date_00_dict_cng[index] else " N|" for day in range(1,len_month+1)])
        table += f'{index_name_cng[index]:>21} 00: |{string_time_00} всего {len(index_date_00_dict_cng[index])}\n'
        # записываем данные о сроках 12
        string_time_12 = ''.join(["__|" if day in index_date_12_dict_cng[index] else " N|" for day in range(1,len_month+1)])
        table += f'{index}{" ":17}12: |{string_time_12} всего {len(index_date_12_dict_cng[index])}\n'
    # считаем суммы выпусков за месяц
    sum_00 = sum([len(index_date_00_dict_cng[index]) for index in indexs])
    sum_12 = sum([len(index_date_12_dict_cng[index]) for index in indexs])
    all_sum = sum_00 + sum_12
    sum_month_cng += all_sum
    table += f'{" ":21}По УГМС всего:{all_sum}\n'
table += f'По УГМС за месяц {sum_month_cng}'




save_report(table, file_name='bnill')
