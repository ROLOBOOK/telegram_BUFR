from base_report import *


# подключаемся к базе получаем список данных за сроки 00 и 12
data_month_00, data_month_12 = load_data_from_bd('oborudovanie, text_info_ValueData_205060')

def work_with_dict_for_type_radio_zond(list_, index_name_dict=index_name_dict):
    '''записываем в словарь даные {индекс_cтанции: {день : данные}} '''
    index_date_dict = {i:{day:'' for day in range(1,month_now + 1)} for i in index_name_dict.keys()}
    for index_day_dicriptor in sorted(list_, key=lambda x: (x[0],x[2])):
        if index_date_dict.get(index_day_dicriptor[0],0):
            if index_day_dicriptor[2].startswith('090'):
                index_date_dict[index_day_dicriptor[0]][index_day_dicriptor[1].day] = index_day_dicriptor[3][-4:]
            else:
                index_date_dict[index_day_dicriptor[0]][index_day_dicriptor[1].day] = index_day_dicriptor[2].split()[0]
    return index_date_dict


index_date_00_dict = work_with_dict_for_type_radio_zond(data_month_00)
index_date_12_dict = work_with_dict_for_type_radio_zond(data_month_12)


# срок|01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|
string_count_day_month = ''.join([f'{i: ^6d}|' for i in range(1,len_month + 1)])
first_string_table = f' срок|{string_count_day_month}'

# проходим по словарю угмс
table = 'Таблица типы радиозондов\n'
for ugms,indexs in sorted(ugms_dict.items()):
    table += f'{ugms}\n{" ":21}{first_string_table}\n'
    # проходим по списку станций в угмс
    for index in sorted(indexs):
    # пишем данные о сроках 00
        string_time_00 = ''.join([f"{index_date_00_dict[index][day]:^6}|" if index_date_00_dict[index].get(day, 0)  else f"{'-':^6}|" for day in range(1,len_month+1)])
        table += f'{index_name_dict[index]:>21} 00: |{string_time_00}\n'
        # записываем данные о сроках 12
        string_time_12 = ''.join([f"{index_date_12_dict[index][day]:^6}|" if index_date_12_dict[index].get(day, 0)  else f"{'-':^6}|" for day in range(1,len_month+1)])
        table += f'{index}{" ":17}12: |{string_time_12}\n'


# для станций СНГ

index_date_00_dict_cng = work_with_dict_for_type_radio_zond(data_month_00, index_name_dict=index_name_cng)
index_date_12_dict_cng = work_with_dict_for_type_radio_zond(data_month_12, index_name_dict=index_name_cng)


for ugms,indexs in sorted(ugm_cng.items()):
    table += f'{ugms}\n{" ":21}{first_string_table}\n'
    # проходим по списку станций в угмс
    for index in sorted(indexs):
    # пишем данные о сроках 00
        string_time_00 = ''.join([f"{index_date_00_dict_cng[index][day]:^6}|" if index_date_00_dict_cng[index].get(day, 0)  else f"{'-':^6}|" for day in range(1,len_month+1)])
        table += f'{index_name_cng[index]:>21} 00: |{string_time_00}\n'
        # записываем данные о сроках 12
        string_time_12 = ''.join([f"{index_date_12_dict_cng[index][day]:^6}|" if index_date_12_dict_cng[index].get(day, 0)  else f"{'-':^6}|" for day in range(1,len_month+1)])
        table += f'{index}{" ":17}12: |{string_time_12}\n'




save_report(table, file_name='bmc')

