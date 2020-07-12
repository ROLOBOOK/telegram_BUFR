from base_report import *


# подключаемся к базе получаем список данных за сроки 00 и 12
data_month_00, data_month_12 = load_data_from_bd('RADIOSONDE_ASCENSION_NUMBER_001082')

index_date_00_dict = work_with_dict(data_month_00)
index_date_12_dict = work_with_dict(data_month_12)


# срок|01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|
string_count_day_month = ''.join([f'{i: 03d}|' for i in range(1,len_month + 1)])
first_string_table = f' срок|{string_count_day_month}'

# проходим по словарю угмс
table = 'Таблица порядковый номер выпуска\n'
for ugms,indexs in sorted(ugms_dict.items()):
    table += f'{ugms}\n{" ":21}{first_string_table}\n'
    # проходим по списку станций в угмс
    for index in sorted(indexs):
    # пишем данные о сроках 00
        string_time_00 = ''.join([f"{index_date_00_dict[index][day]:>3}|" if index_date_00_dict[index].get(day, 0)  else " - |" for day in range(1,len_month+1)])
        table += f'{index_name_dict[index]:>21} 00: |{string_time_00}\n'
        # записываем данные о сроках 12
        string_time_12 = ''.join([f"{index_date_12_dict[index][day]:>3}|" if index_date_12_dict[index].get(day, 0)  else " - |" for day in range(1,len_month+1)])
        table += f'{index}{" ":17}12: |{string_time_12}\n'
    # считаем суммы выпусков за месяц


#  для станций СНГ
index_date_00_dict_cng = work_with_dict(data_month_00,index_name_dict=index_name_cng)
index_date_12_dict_cng = work_with_dict(data_month_12, index_name_dict=index_name_cng)

for ugms,indexs in sorted(ugm_cng.items()):
    table += f'{ugms}\n{" ":21}{first_string_table}\n'
    # проходим по списку станций в угмс
    for index in sorted(indexs):
    # пишем данные о сроках 00
        string_time_00 = ''.join([f"{index_date_00_dict_cng[index][day]:>3}|" if index_date_00_dict_cng[index].get(day, 0)  else " - |" for day in range(1,len_month+1)])
        table += f'{index_name_cng[index]:>21} 00: |{string_time_00}\n'
        # записываем данные о сроках 12
        string_time_12 = ''.join([f"{index_date_12_dict_cng[index][day]:>3}|" if index_date_12_dict_cng[index].get(day, 0)  else " - |" for day in range(1,len_month+1)])
        table += f'{index}{" ":17}12: |{string_time_12}\n'
    # считаем суммы выпусков за месяц






save_report(table,file_name='bmn')

