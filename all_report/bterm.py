from base_report import *



def work_with_dict(list_):
#'''записываем в словарь даные {индекс_cтанции: {день : данные}} '''
    index_date_dict = {i:[] for i in index_name_dict.keys()}
    for index_day_dicriptor in list_:
        if index_day_dicriptor[0] in index_date_dict:
            index_date_dict[index_day_dicriptor[0]].append(index_day_dicriptor[1:])
    return index_date_dict

def make_row (number,index, index_date_dic):
    row = ''
#    print(index, *sorted([i[:2] for i in index_date_dic[index]],key=lambda x: x[0],reverse=True),sep='\n')
    for data_srok in sorted(index_date_dic[index]):
        date = data_srok[0].strftime('%Y-%m-%d')
        srok = data_srok[0].strftime('%H')
        temp_kod_zonda = data_srok[1].split()[0]
        kod_zonda = temp_kod_zonda if temp_kod_zonda != '090' else data_srok[2].split()[-1][1:]
        reason_end = data_srok[-1]
        if reason_end not in list_tetm_2:
            continue
        row+= f'|{number:^3}|{index:^7}|{date:10}|{srok:^4}|{kod_zonda:^9}|{reason_end:^17}|\n'
        number +=1
    return row, number

#делаем словарь для подсчета причина окончания выпуска - тип зонда - количество в месяц
dic_index_ugms = {data[0]:data[-1] for data in rr}
list_temp = ['027', '128','129','053', '058', '160','162','068','069','075', '076', '088', '089','03','119']
dic_temp_1 = {i:0 for i in list_temp}
list_tetm_2 = ['4','5','8','9','11','12','14','15','17', '1','2','3','6','7','30']
dic_temp_2 = {i:{i:0 for i in list_temp} for i in list_tetm_2}
ugms_with_sum = {ugms:{i:{i:0 for i in list_temp} for i in list_tetm_2} for ugms in ugms_list}

def count_(index_date_dict):
    for index, data in index_date_dict.items():
    #('34731', [(datetime.datetime(2020, 5, 5, 0, 0), '162 05 003 03', '61616 10000', '8')])
        for data_list in data:
            ugms = dic_index_ugms[index]
            reason_end = data_list[-1]
            if reason_end not in list_tetm_2:
                continue
            type_zonda = data_list[1].split()[0] if data_list[1].split()[0] != '090' else '03'
            ugms_with_sum[ugms][reason_end][type_zonda]+=1

with open('/home/bufr/bufr_work/telegram_BUFR/for_work/name_ugms.txt', 'r') as f:
    text = f.read()
ugms_name = {i.split()[0]:i.split()[-1] for i in text.split('\n') if i}


data_month_00, data_month_12 = load_data_from_bd('oborudovanie, text_info_ValueData_205060, descriptor_035035')

index_date_00_dict = work_with_dict(data_month_00)
index_date_12_dict = work_with_dict(data_month_12)

# заполняем словарь ugms_with_sum

count_(index_date_00_dict)
count_(index_date_12_dict)


for ugms,indexs in sorted(ugms_dict.items()):


    table = f'{ugms}\n{"-"*57}\n|№/№|станция|   дата   |срок|код зонда|причина окончания|\n{"-"*57}\n'
    number = 1
    for index in indexs:
        row,number =  make_row(number,index,index_date_00_dict)
        table += row
        row, number= make_row(number,index,index_date_12_dict)
        table += row
    table += f'{"-"*57}\n\n'


    table2 = f'{"-"*82}\nИтого|' + ''.join([f'{i:^4}|' for i in list_temp[:-1]]) + f'03xx|\n{"-"*82}\n'
    for reason, type_zonda in ugms_with_sum[ugms].items():
        empty = ' '
        row_type_zond = ''.join([f'{type_zonda[i]:^4}|' if type_zonda[i] else f"{empty:4}|" for i in list_temp])
        table2 += f'{reason:^5}|{row_type_zond}\n'

    table2 += f"{'-'*82}"
    table += table2
    table+= '''\n\n\n1\tРазрыв оболочки\n2\tОбледенение оболочки\n3\tЗависание оболочки\n6\tОтказ наземного оборудования\n7\tРадиопомехи
13\tПринудительное прекращение\n30\tДругие причины\n\n4\tЗатухание/пропажа сигнала\n5\tОтказ батареи\n8\tОтказ радиозонда\n9\tПропуски/разброс телеметирии
11\tПропуски темпертаруты\n14\tПропал сигнал\n15\tСрыв сопровождения\n17\tДлительные пропуски или недостоверные данные\n'''
    dir_list = os.listdir('/home/bufr/reports')
    dir_month_now = f'report_{month_now:02d}{now.year}'
    if dir_month_now not in dir_list:
        os.mkdir(f'/home/bufr/reports/{dir_month_now}')
    dir_list_in_folder = os.listdir(f'/home/bufr/reports/{dir_month_now}')
    folder_Termination = 'Termination'
    if folder_Termination not in dir_list_in_folder:
        os.mkdir(f'/home/bufr/reports/{dir_month_now}/{folder_Termination}')
    with open(f'/home/bufr/reports/{dir_month_now}/{folder_Termination}/{ugms_name[ugms]}.bterm', 'w') as f:
        f.write(table)
