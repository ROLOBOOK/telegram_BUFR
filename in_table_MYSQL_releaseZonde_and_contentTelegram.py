# !/usr/bin/env python3

# заполняем таблицу tsao.content_telegram и releaseZonde с данными наблюдений:


import os, MySQLdb
from pybufrkit.renderer import FlatJsonRenderer
from pybufrkit.decoder import Decoder    
    
def get_data_from_BUFR(data, date='0000-00-00 00:00:00'):
    
    '''получаем данные для таблицы tsao.content_telegram с данными наблюдений'''
    
    index_station = '{}{:03d}'.format(data[27],data[28])
    
    data_in_table = []
    sloi = []
    for i in range(0,len(data[56:]),10):
        sloi.append(data[56:][i:i+10])
    sloi = sloi[:-1]

    for i in range(len(sloi)):
        if type(sloi[i][6]) == float:
            sloi[i][6] = round(sloi[i][6] - 273.15, 2)
        else:
            sloi[i][6] = None
        if type(sloi[i][7]) == float:
            sloi[i][7] = round(sloi[i][7] - 273.15, 2)
        else:
            sloi[i][7] = None
        if type(sloi[i][0]) != int:
            sloi[i][0] = None
        if type(sloi[i][1]) != int:
            sloi[i][1] = None
        if type(sloi[i][2]) == float:
            sloi[i][2] = round(sloi[i][2]/100, 1)
        else:
            sloi[i][2] = None
        if type(sloi[i][3]) != int:
            sloi[i][3] = None
        if type(sloi[i][4]) != float:
            sloi[i][4] = None
        if type(sloi[i][5]) != float:
            sloi[i][5] = None
        if type(sloi[i][6]) != float:
            sloi[i][6] = None
        if type(sloi[i][7]) != float:
            sloi[i][7] = None
        if type(sloi[i][8]) != int:
            sloi[i][8] = None
        if type(sloi[i][9]) != float:
            sloi[i][9] = None
        data_in_table.append((index_station, date, sloi[i][0], sloi[i][2], sloi[i][6], sloi[i][7], sloi[i][3], sloi[i][8], sloi[i][9], sloi[i][4], sloi[i][5], sloi[i][1],))

#     t = 0  flag = 1    P = 2    H = 3    dflat = 4    dlon = 5    T = 6    Td = 7    V = 9    D = 8
   
    return  data_in_table
 

def get_data_for_table_releaseZonde(data, date='0000-00-00 00:00:00'):


    ''' получаем данные для таблицы releaseZonde''' 

    index_station = '{}{:03d}'.format(data[27],data[28]) # индекс станции
    coordinateStation = ' '.join(map(str, data[41:46])) # координаты станции
    oborudovanie = data[30]
    zond = data[-1].decode('utf-8').split()[-1] if type(data[-1]) == bytes else None
    oborudovanie_zond = f'{oborudovanie} {zond}' #  оборудование + текстовая информация
    device = ' '.join(map(str, data[30:34])) # оборудование вся строка
    height = data[23] # высота станици 
    number_look = data[1] # # Номер наблюдения(001082):421
    lengthOfTheSuspension = data[15]  # # Длина подвеса к оболочке(002086):13.00
    amountOfGas  = data[14]  # # Количество газа используемого в радиозондовой оболочке(002085):1.200
    gasForFillingTheShell = data[13] # # Газ для наполнения оболочки(002084):0
    filling = data[12] # # Наполнительная(002083):14
    weightOfTheShell  = data[11] # # Масса оболочки(002082):0.50
    typeShell  = data[10] # # Тип оболочки(002081):0
    radiosondeShellManufacturer  = data[9] # # Производитель радиозондовой оболочки(002080):4
    configurationOfRadiosondeSuspension  = data[5] # # Конфигурация подвески радиозонда(002016):0
    configurationOfTheRadiosonde = data[4] # # Конфигурация радиозонда(002015):4
    typeOfHumiditySensor  = data[18] # # Тип датчика влажности(002097):4
    temperatureSensorType  = data[17]    # # Тип датчика температуры(002096):0
    pressureSensorType= data[16] # Тип датчика давления(002095):4
    carrierFrequency = round(int(data[8])/10**6, 3) # Несущая частота(002067):1680.000
    text_info = data[-1].decode('utf-8') if type(data[-1]) == bytes else None  # Текстовая информация:61616 20312
    s_n_zonda = data[0].decode('Windows-1251').replace(' ', '') if type(data[0]) == bytes else None # Серийный номеррадиозонда(001081):2279784/0586 
    PO_versia = data[21].decode('utf-8').replace(' ', '') if type(data[21]) == bytes else None  # ПО, версия(025061):212/20152   
    MethodGeopotentialHeight = data[20] # Метод определения геопотенциальной высоты(002191):2
    ugol = json_data[3][2][0][26] # # Поправка к ориентации по углу места(025066):359.00
    azimut = data[25] # Поправка к ориентации по азимуту(025065):84.50
    h_opor = data[24] # # Высота антенны над основанием опоры(002102):8.0
    groundBasedRradiosondeSignalReceptionSystem = data[7] # # Наземная система приема сигналов радиозондов(002066):6
    identificator = data[3].decode('utf-8').replace(' ', '') if type(data[3]) == bytes else None # # Идентификация наблюдателей(001095):IGP 
    sensingNnumber = data[2] # # Номер зондирования(001083):1

    return (index_station, date, coordinateStation, oborudovanie_zond, height, number_look, lengthOfTheSuspension, 
            amountOfGas, gasForFillingTheShell, filling, weightOfTheShell, typeShell, radiosondeShellManufacturer,
            configurationOfRadiosondeSuspension, configurationOfTheRadiosonde, typeOfHumiditySensor, temperatureSensorType,
           pressureSensorType, carrierFrequency, text_info, s_n_zonda, PO_versia, MethodGeopotentialHeight, ugol, azimut, h_opor,
           groundBasedRradiosondeSignalReceptionSystem, identificator, sensingNnumber)

# номерстанции дата время P T Td H D V dLat dLon Flags
# Stations_numberStation date time  P T Td H D V dLat dLon Flags



# получаем файлы из папки "./" 
try:
#     files = os.listdir(path="./")
    files = [file for file in os.listdir(path="./") if file[-3:] == 'bin']
except:
    print("ошибка получения списков файлов для расшифровки")

    
# подключаемся к базе для записи в таблицу  table1 с данными наблюдений
try:
    conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'tsao', charset="utf8")
    cursor = conn.cursor()

# декодируем burf в юникод
    for file_name in files:
        try:
            decoder = Decoder()
            with open(f'./{file_name}', 'rb') as ins: #
                bufr_message = decoder.process(ins.read())
            json_data = FlatJsonRenderer().render(bufr_message)
        except:
            print('не декодирован')
            
# тут обрабатываем json_data     
        d = '{}-{:02d}-{:02d}'.format(json_data[1][-6], json_data[1][-5], json_data[1][-4])
        t = '{:02d}:{:02d}:{:02d}'.format(json_data[1][-3], json_data[1][-2], json_data[1][-1] )
        date = f'{d} {t}' # дата и срок выпуска
        
        for data in json_data[3][2]:

            data_in_releaseZonde = get_data_for_table_releaseZonde(data, date)
            
            cursor.execute('''INSERT INTO tsao.releaseZonde
            (Stations_numberStation, date, coordinateStation, oborudovanie_zond, height, number_look, lengthOfTheSuspension, 
            amountOfGas, gasForFillingTheShell, filling, weightOfTheShell, typeShell, radiosondeShellManufacturer,
            configurationOfRadiosondeSuspension, configurationOfTheRadiosonde, typeOfHumiditySensor, temperatureSensorType,
           pressureSensorType, carrierFrequency, text_info, s_n_zonda, PO_versia, MethodGeopotentialHeight, ugol, azimut, h_opor,
           groundBasedRradiosondeSignalReceptionSystem, identificator, sensingNnumber)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',data_in_releaseZonde)
            conn.commit()
            data_in_content_telegram = get_data_from_BUFR(data, date)
#             заносим данные в таблицу tsao.content_telegram
            cursor.executemany('''INSERT INTO tsao.content_telegram (Stations_numberStation, date, time, P, T, Td, H, D, V, dLat, dLon, Flags)  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',data_in_content_telegram)
            conn.commit()

            

except Exception as ex:
    print(ex)

# Разрываем подключение.
finally:
    conn.close()