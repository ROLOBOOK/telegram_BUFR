from base_report import *
from collections import Counter
import sys, paramiko, os

sys.path.insert(1, '../for_work')

from ssh_webserver import server,name,password,port


name_month = {1:'январь',2:'февраль',3:'март',4:'апрель',5:'май',6:'июнь',7:'июль',8:'август',9:'сентябрь',10:'октябрь',11:'ноябрь',12:'декабрь'}

def get_data_from_bd(table='releaseZonde', columns='Stations_numberStation', criterion='',month=month_now):
    conn = MySQLdb.connect('localhost', 'fol', 'Qq123456', 'cao_bufr_v2', charset="utf8")
    cursor = conn.cursor()
    cursor.execute(f'''select {columns} from cao_bufr_v2.{table} {criterion};''')
    data = cursor.fetchall()
    conn.close()
    return data



count_pusk_month = get_data_from_bd(columns='Stations_numberStation, count(Stations_numberStation)',
                                    criterion=f'where month(time_srok)={month_now} group by Stations_numberStation')

avg_H_month = get_data_from_bd(columns='Stations_numberStation, time_srok, H', table='last_H',
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

#для СНГ
#считаем количество типов радиозондов
count_type_zonds_cng = {i:[] for i in index_name_cng}
[count_type_zonds_cng[i[0]].append(i[1][:3]) for i in count_type_zonde_month if i[0] in count_type_zonds_cng]
counter_type = {i:Counter(count_type_zonds_cng[i]) for i in count_type_zonds_cng if count_type_zonds_cng[i]}

#
count_end_pusk_cng = {i:[] for i in index_name_cng}
[count_end_pusk_cng[i[0]].append(i[1]) for i in count_end_month if i[0] in count_end_pusk_cng]
counter_end_cng = {i:Counter(count_end_pusk_cng[i]) for i in count_end_pusk_cng if count_end_pusk_cng[i]}

#добавляем количество зондов и процент
dict_cng = {i[0]:[i[1],round(i[1] / (len_month*2) * 100,2)] for i in  count_pusk_month if i[0] in index_name_cng}
#добавляем  среднюю высоту
[dict_cng[i[0]].append(int(i[1])) for i in avg_H_month if i[0] in index_name_cng]
#добавляем количество типов выпущеных зондов
[dict_cng[i].append(counter_type[i]) for i in dict_cng]
#добавляем  количесвто присины окончания
[dict_cng[i].append(counter_end_cng[i]) for i in dict_cng]



head = '''
<html xmlns:o="urn:schemas-microsoft-com:office:office"
xmlns:x="urn:schemas-microsoft-com:office:excel"
xmlns="http://www.w3.org/TR/REC-html40">

<head>
<meta http-equiv=Content-Type content="text/html; charset=utf-8">
<meta name=ProgId content=Excel.Sheet>
<meta name=Generator content="Microsoft Excel 14">
<link rel=File-List href="repbufr2020_06.files/filelist.xml">
<style id="сводная_шаблон_21853_Styles">
	{mso-displayed-decimal-separator:"\.";
	mso-displayed-thousand-separator:" ";}
.xl6621890
	{padding-top:1px;
	padding-right:1px;
	padding-left:1px;
	mso-ignore:padding;
	color:black;
	font-size:12.0pt;
	font-weight:400;
	font-style:normal;
	text-decoration:none;
	font-family:"Times New Roman", serif;
	mso-font-charset:204;
	mso-number-format:General;
	text-align:center;
	vertical-align:middle;
	border:.5pt solid windowtext;
	background:#FFA500;
	mso-pattern:black none;
	white-space:nowrap;}
.xl6321853
	{padding-top:1px;
	padding-right:1px;
	padding-left:1px;
	mso-ignore:padding;
	color:black;
	font-size:12.0pt;
	font-weight:400;
	font-style:normal;
	text-decoration:none;
	font-family:"Times New Roman", serif;
	mso-font-charset:204;
	mso-number-format:General;
	text-align:center;
	vertical-align:middle;
	mso-background-source:auto;
	mso-pattern:auto;
	white-space:nowrap;}
.xl6421853
	{padding-top:1px;
	padding-right:1px;
	padding-left:1px;
	mso-ignore:padding;
	color:black;
	font-size:12.0pt;
	font-weight:400;
	font-style:normal;
	text-decoration:none;
	font-family:"Times New Roman", serif;
	mso-font-charset:204;
	mso-number-format:General;
	text-align:center;
	vertical-align:middle;
	border:.5pt solid windowtext;
	mso-background-source:auto;
	mso-pattern:auto;
	white-space:nowrap;}
.xl6521853
	{padding-top:1px;
	padding-right:1px;
	padding-left:1px;
	mso-ignore:padding;
	color:black;
	font-size:12.0pt;
	font-weight:400;
	font-style:normal;
	text-decoration:none;
	font-family:"Times New Roman", serif;
	mso-font-charset:204;
	mso-number-format:General;
	text-align:center;
	vertical-align:middle;
	border:.5pt solid windowtext;
	mso-background-source:auto;
	mso-pattern:auto;
	white-space:normal;}
.xl6621853
	{padding-top:1px;
	padding-right:1px;
	padding-left:1px;
	mso-ignore:padding;
	color:black;
	font-size:12.0pt;
	font-weight:400;
	font-style:normal;
	text-decoration:none;
	font-family:"Times New Roman", serif;
	mso-font-charset:204;
	mso-number-format:General;
	text-align:center;
	vertical-align:middle;
	border:.5pt solid windowtext;
	background:#C5D9F1;
	mso-pattern:black none;
	white-space:nowrap;}
.xl6721853
	{padding-top:1px;
	padding-right:1px;
	padding-left:1px;
	mso-ignore:padding;
	color:black;
	font-size:12.0pt;
	font-weight:400;
	font-style:normal;
	text-decoration:none;
	font-family:"Times New Roman", serif;
	mso-font-charset:204;
	mso-number-format:General;
	text-align:left;
	vertical-align:middle;
	mso-background-source:auto;
	mso-pattern:auto;
	white-space:nowrap;}
.xl6821853
	{padding-top:1px;
	padding-right:1px;
	padding-left:1px;
	mso-ignore:padding;
	color:black;
	font-size:14.0pt;
	font-weight:400;
	font-style:normal;
	text-decoration:none;
	font-family:"Times New Roman", serif;
	mso-font-charset:204;
	mso-number-format:General;
	text-align:center;
	vertical-align:middle;
	mso-background-source:auto;
	mso-pattern:auto;
	white-space:nowrap;}
.xl6921853
	{padding-top:1px;
	padding-right:1px;
	padding-left:1px;
	mso-ignore:padding;
	color:black;
	font-size:12.0pt;
	font-weight:400;
	font-style:normal;
	text-decoration:none;
	font-family:"Times New Roman", serif;
	mso-font-charset:204;
	mso-number-format:General;
	text-align:left;
	vertical-align:middle;
	border:.5pt solid windowtext;
	mso-background-source:auto;
	mso-pattern:auto;
	white-space:nowrap;}
.xl7021853
	{padding-top:1px;
	padding-right:1px;
	padding-left:1px;
	mso-ignore:padding;
	color:black;
	font-size:12.0pt;
	font-weight:400;
	font-style:normal;
	text-decoration:none;
	font-family:"Times New Roman", serif;
	mso-font-charset:204;
	mso-number-format:General;
	text-align:center;
	vertical-align:middle;
	border-top:.5pt solid windowtext;
	border-right:none;
	border-bottom:none;
	border-left:.5pt solid windowtext;
	mso-background-source:auto;
	mso-pattern:auto;
	white-space:normal;}
.xl7121853
	{padding-top:1px;
	padding-right:1px;
	padding-left:1px;
	mso-ignore:padding;
	color:black;
	font-size:12.0pt;
	font-weight:400;
	font-style:normal;
	text-decoration:none;
	font-family:"Times New Roman", serif;
	mso-font-charset:204;
	mso-number-format:General;
	text-align:center;
	vertical-align:middle;
	border-top:.5pt solid windowtext;
	border-right:none;
	border-bottom:none;
	border-left:none;
	mso-background-source:auto;
	mso-pattern:auto;
	white-space:normal;}
.xl7221853
	{padding-top:1px;
padding-right:1px;
	padding-left:1px;
	mso-ignore:padding;
	color:black;
	font-size:12.0pt;
	font-weight:400;
	font-style:normal;
	text-decoration:none;
	font-family:"Times New Roman", serif;
	mso-font-charset:204;
	mso-number-format:General;
	text-align:center;
	vertical-align:middle;
	border-top:.5pt solid windowtext;
	border-right:.5pt solid windowtext;
	border-bottom:none;
	border-left:none;
	mso-background-source:auto;
	mso-pattern:auto;
	white-space:normal;}
.xl7321853
	{padding-top:1px;
	padding-right:1px;
	padding-left:1px;
	mso-ignore:padding;
	color:black;
	font-size:12.0pt;
	font-weight:400;
	font-style:normal;
	text-decoration:none;
	font-family:"Times New Roman", serif;
	mso-font-charset:204;
	mso-number-format:General;
	text-align:center;
	vertical-align:middle;
	border-top:none;
	border-right:none;
	border-bottom:.5pt solid windowtext;
	border-left:.5pt solid windowtext;
	mso-background-source:auto;
	mso-pattern:auto;
	white-space:normal;}
.xl7421853
	{padding-top:1px;
	padding-right:1px;
	padding-left:1px;
	mso-ignore:padding;
	color:black;
	font-size:12.0pt;
	font-weight:400;
	font-style:normal;
	text-decoration:none;
	font-family:"Times New Roman", serif;
	mso-font-charset:204;
	mso-number-format:General;
	text-align:center;
	vertical-align:middle;
	border-top:none;
	border-right:none;
	border-bottom:.5pt solid windowtext;
	border-left:none;
	mso-background-source:auto;
	mso-pattern:auto;
	white-space:normal;}
.xl7521853
	{padding-top:1px;
	padding-right:1px;
	padding-left:1px;
	mso-ignore:padding;
	color:black;
	font-size:12.0pt;
	font-weight:400;
	font-style:normal;
	text-decoration:none;
	font-family:"Times New Roman", serif;
	mso-font-charset:204;
	mso-number-format:General;
	text-align:center;
	vertical-align:middle;
	border-top:none;
	border-right:.5pt solid windowtext;
	border-bottom:.5pt solid windowtext;
	border-left:none;
	mso-background-source:auto;
	mso-pattern:auto;
	white-space:normal;}
.xl7621853
	{padding-top:1px;
	padding-right:1px;
	padding-left:1px;
	mso-ignore:padding;
	color:black;
	font-size:12.0pt;
	font-weight:400;
	font-style:normal;
	text-decoration:none;
	font-family:"Times New Roman", serif;
	mso-font-charset:204;
	mso-number-format:General;
	text-align:center;
	vertical-align:middle;
	border-top:.5pt solid windowtext;
	border-right:.5pt solid windowtext;
	border-bottom:none;
	border-left:.5pt solid windowtext;
	mso-background-source:auto;
	mso-pattern:auto;
	white-space:nowrap;}
.xl7721853
	{padding-top:1px;
	padding-right:1px;
	padding-left:1px;
	mso-ignore:padding;
	color:black;
	font-size:12.0pt;
	font-weight:400;
	font-style:normal;
	text-decoration:none;
	font-family:"Times New Roman", serif;
	mso-font-charset:204;
	mso-number-format:General;
	text-align:center;
	vertical-align:middle;
	border-top:none;
	border-right:.5pt solid windowtext;
	border-bottom:none;
	border-left:.5pt solid windowtext;
	mso-background-source:auto;
	mso-pattern:auto;
	white-space:nowrap;}
.xl7821853
	{padding-top:1px;
	padding-right:1px;
	padding-left:1px;
	mso-ignore:padding;
	color:black;
	font-size:12.0pt;
	font-weight:400;
	font-style:normal;
	text-decoration:none;
	font-family:"Times New Roman", serif;
	mso-font-charset:204;
	mso-number-format:General;
	text-align:center;
	vertical-align:middle;
	border-top:none;
	border-right:.5pt solid windowtext;
	border-bottom:.5pt solid windowtext;
	border-left:.5pt solid windowtext;
	mso-background-source:auto;
	mso-pattern:auto;
	white-space:nowrap;}
.xl7921853
	{padding-top:1px;
	padding-right:1px;
	padding-left:1px;
	mso-ignore:padding;
	color:black;
	font-size:12.0pt;
	font-weight:400;
	font-style:normal;
	text-decoration:none;
	font-family:"Times New Roman", serif;
	mso-font-charset:204;
	mso-number-format:General;
	text-align:center;
	vertical-align:middle;
	border-top:.5pt solid windowtext;
	border-right:.5pt solid windowtext;
	border-bottom:none;
	border-left:.5pt solid windowtext;
	mso-background-source:auto;
	mso-pattern:auto;
	white-space:normal;}
.xl8021853
	{padding-top:1px;
	padding-right:1px;
	padding-left:1px;
	mso-ignore:padding;
	color:black;
	font-size:12.0pt;
	font-weight:400;
	font-style:normal;
	text-decoration:none;
	font-family:"Times New Roman", serif;
	mso-font-charset:204;
	mso-number-format:General;
	text-align:center;
	vertical-align:middle;
	border-top:none;
	border-right:.5pt solid windowtext;
	border-bottom:.5pt solid windowtext;
	border-left:.5pt solid windowtext;
	mso-background-source:auto;
	mso-pattern:auto;
	white-space:normal;}
-->
</style>
</head>'''

body = f'''<body>
<a href=../../{year_now}/{month_now-1:02}/{year_now}{month_now-1:02}.html>Предыдущий месяц</a>&nbsp;|&nbsp;<a href=../../{year_now}/{month_now+1:02}/{year_now}{month_now+1:02}.html>Следующий месяц</a>&nbsp;|&nbsp;<a href="http://cao-ntcr.mipt.ru/monitor/monitorbufr.htm">На верхний уровень</a>
<hr>

<div id="сводная_шаблон_21853" align=center x:publishsource="Excel">

<table border=0 cellpadding=0 cellspacing=0 width=1382 class=xl6821853
 style='border-collapse:collapse;table-layout:fixed;width:1038pt'>
 <col class=xl6821853 width=201 style='mso-width-source:userset;mso-width-alt:
 7350;width:151pt'>
 <col class=xl6821853 width=71 span=2 style='mso-width-source:userset;
 mso-width-alt:2596;width:53pt'>
 <col class=xl6821853 width=103 style='mso-width-source:userset;mso-width-alt:
 3766;width:77pt'>
 <col class=xl6821853 width=77 span=6 style='mso-width-source:userset;
 mso-width-alt:2816;width:58pt'>
 <col class=xl6821853 width=90 style='mso-width-source:userset;mso-width-alt:
 3291;width:68pt'>
 <col class=xl6821853 width=64 span=6 style='width:48pt'>
 <tr height=25 style='height:18.75pt'>
  <td height=25 class=xl6821853 width=201 style='height:18.75pt;width:151pt'></td>
  <td class=xl6821853 width=71 style='width:53pt'></td>
  <td class=xl6821853 width=71 style='width:53pt'></td>
  <td class=xl6821853 width=103 style='width:77pt'></td>
  <td class=xl6821853 width=77 style='width:58pt'></td>
  <td class=xl6821853 width=77 style='width:58pt'></td>
  <td class=xl6821853 width=77 style='width:58pt'></td>
  <td class=xl6821853 width=77 style='width:58pt'></td>
  <td class=xl6821853 width=77 style='width:58pt'></td>
  <td class=xl6821853 width=77 style='width:58pt'></td>
  <td class=xl6821853 width=90 style='width:68pt'></td>
  <td class=xl6821853 width=64 style='width:48pt'></td>
  <td class=xl6821853 width=64 style='width:48pt'></td>
  <td class=xl6821853 width=64 style='width:48pt'></td>
  <td class=xl6821853 width=64 style='width:48pt'></td>
  <td class=xl6821853 width=64 style='width:48pt'></td>
  <td class=xl6821853 width=64 style='width:48pt'></td>
 </tr>
 <tr height=25 style='height:18.75pt'>
  <td colspan=17 height=25 class=xl6821853 style='height:18.75pt'>Сводная
  информация о функционировании аэрологической сети РФ, по данным телеграмм
  BUFR за {name_month[month_now]} {year_now}г.,</td>
 </tr>
 <tr height=25 style='height:18.75pt'>
 <td colspan=17 height=25 class=xl6821853 style='height:18.75pt' >сформирована на {now.strftime('%d.%m.%y')}</td>
 </tr> <tr height=25 style='height:18.75pt'>
  <td height=25 class=xl6821853 style='height:18.75pt'></td>
  <td class=xl6821853></td>
  <td class=xl6821853></td>
  <td class=xl6821853></td>
  <td class=xl6821853></td>
  <td class=xl6821853></td>
  <td class=xl6821853></td>
  <td class=xl6821853></td>
  <td class=xl6821853></td>
  <td class=xl6821853></td>
  <td class=xl6821853></td>
  <td class=xl6821853></td>
  <td class=xl6821853></td>
  <td class=xl6821853></td>
  <td class=xl6821853></td>
  <td class=xl6821853></td>
  <td class=xl6821853></td>
 </tr>
 <tr height=25 style='height:18.75pt'>
  <td rowspan=3 height=92 class=xl7621853 style='border-bottom:.5pt solid black;
  height:69.0pt'>Станции/Управления</td>
  <td colspan=2 rowspan=2 class=xl7021853 width=142 style='border-right:.5pt solid black;
  border-bottom:.5pt solid black;width:106pt'><span
  style='mso-spacerun:yes'>    </span>Поступление телеграмм в BUFR<span
  style='mso-spacerun:yes'>   </span></td>
  <td rowspan=2 class=xl7921853 width=103 style='border-bottom:.5pt solid black;
  width:77pt'>Высота<span style='mso-spacerun:yes'>   </span>зондирования</td>
  <td colspan=7 rowspan=2 class=xl7021853 width=552 style='border-right:.5pt solid black;
  border-bottom:.5pt solid black;width:416pt'>Количество выпущеный радиозондов
  по телеграммам BUFR<span style='mso-spacerun:yes'>        </span></td>
  <td colspan=6 rowspan=2 class=xl6521853 width=384 style='width:288pt'>Количество
  выпусков,<span style='mso-spacerun:yes'>  </span>которые закончились<span
  style='mso-spacerun:yes'>     </span></td>
 </tr>
 <tr height=25 style='height:18.75pt'>
 </tr>
 <tr height=42 style='height:31.5pt'>
  <td height=42 class=xl6421853 style='height:31.5pt;border-top:none;
  border-left:none'><span style='mso-spacerun:yes'> </span>кол-во<span
  style='mso-spacerun:yes'> </span></td>
  <td class=xl6421853 style='border-top:none;border-left:none'><span
  style='mso-spacerun:yes'> </span>%, плана<span
  style='mso-spacerun:yes'> </span></td>
  <td class=xl6421853 style='border-top:none;border-left:none'><span
  style='mso-spacerun:yes'>     </span>м<span
  style='mso-spacerun:yes'>      </span></td>
  <td class=xl6421853 style='border-top:none;border-left:none'><span
  style='mso-spacerun:yes'> </span>МРЗ-3АК<span
  style='mso-spacerun:yes'> </span></td>
  <td class=xl6421853 style='border-top:none;border-left:none'><span
  style='mso-spacerun:yes'> </span>МРЗ-3МК<span
  style='mso-spacerun:yes'> </span></td>
  <td class=xl6421853 style='border-top:none;border-left:none'><span
  style='mso-spacerun:yes'> </span>МРЗ-Н1<span
  style='mso-spacerun:yes'> </span></td>
  <td class=xl6421853 style='border-top:none;border-left:none'><span
  style='mso-spacerun:yes'> </span>АК2-02м<span
  style='mso-spacerun:yes'> </span></td>
  <td class=xl6421853 style='border-top:none;border-left:none'><span
  style='mso-spacerun:yes'> </span>РЗМ-2</td>
  <td class=xl6421853 style='border-top:none;border-left:none'><span
  style='mso-spacerun:yes'> </span>И-2012</td>
  <td class=xl6521853 width=90 style='border-top:none;border-left:none;
  width:68pt'>Ошибочный код</td>
  <td class=xl6421853 style='border-top:none;border-left:none'>&quot;1&quot;</td>
  <td class=xl6421853 style='border-top:none;border-left:none'>&quot;6&quot;</td>
  <td class=xl6421853 style='border-top:none;border-left:none'>&quot;7&quot;</td>
  <td class=xl6421853 style='border-top:none;border-left:none'>&quot;8&quot;</td>
  <td class=xl6421853 style='border-top:none;border-left:none'>&quot;14&quot;</td>
  <td class=xl6421853 style='border-top:none;border-left:none'>прочее</td>
 </tr>
'''

html = head + body


rf = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
for ugms,stations in sorted(ugms_dict.items()):
    ugms_sum = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
    for index in sorted(stations,key=lambda x:index_name_dict[x]):
        html += f'''
 <tr height=25 style='height:18.75pt'>
  <td height=25 class=xl6921853 style='height:18.75pt;border-top:none'>{index_name_dict[index]}<span
  style='mso-spacerun:yes'>               </span></td>
'''

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

            list_one_row = [dict_[index][0],dict_[index][1],dict_[index][2],mp3_pak,mp3_3mk,mp3_h1,ak2_2m,p3m_2,u_2012,mistake_cod,one,six,seven,eight,fortin,other]

            [ugms_sum[i].append(zond) for i,zond in enumerate((mp3_pak,mp3_3mk,mp3_h1,ak2_2m,p3m_2,u_2012,mistake_cod,one,six,seven,eight,fortin,other))]

            for  column in list_one_row:
                html += f"<td class=xl6421853 style='border-top:none;border-left:none'>{column}</td>"
        else:
            for _ in range(16):
                html += f"<td class=xl6421853 style='border-top:none;border-left:none'>0</td>"
        html += '</tr>'

    sum_h_ugms = sum([dict_[index][0] for index in stations if index in dict_])
    sum_plan = round(sum_h_ugms/(len_month*2*len(stations)) * 100,2)
    h =[dict_[index][2] for index in stations if index in dict_] 
    midl_h = str(sum(h)// len(h)) if len(h) else 0
    list_ugms_row = [sum_h_ugms,sum_plan,midl_h,sum(ugms_sum[0]),sum(ugms_sum[1]),sum(ugms_sum[2]),sum(ugms_sum[3]),sum(ugms_sum[4]),sum(ugms_sum[5]),sum(ugms_sum[6]),sum(ugms_sum[7]),sum(ugms_sum[8]),sum(ugms_sum[9]),sum(ugms_sum[10]),sum(ugms_sum[11]),sum(ugms_sum[12])]

    html += f'''<tr height=25 style='height:18.75pt'>
  <td height=25 class=xl6621853 style='height:18.75pt;border-top:none'>{ugms}/{len(stations)}</td>'''
    for column in list_ugms_row:
        html += f'''<td class=xl6621853 style='border-top:none;border-left:none'>{column}</td>'''
    html += '</tr>'

    all_in_list = [sum_h_ugms,sum_plan,midl_h] + [i[0] for i in ugms_sum if i]
    [rf[i].append(counts) for i,counts in enumerate(all_in_list)]

all_stations = []
for stations in ugms_dict.values():
    for  i in stations:
        all_stations.append(i)

list_rf_row = [sum(rf[0]),round(sum(rf[0])/(len_month*2*len(all_stations)) * 100,2),sum([int(i) for i in rf[2]])//len(rf[2]),sum(rf[3]),sum(rf[4]),sum(rf[5]),sum(rf[6]),sum(rf[7]),sum(rf[8]),sum(rf[9]),sum(rf[10]),sum(rf[11]),sum(rf[12]),sum(rf[13]),sum(rf[14]),sum(rf[15])]

html += f'''<td height=25 class=xl6621890 style='height:18.75pt;border-top:none'>По
  РФ<span style='mso-spacerun:yes'>          </span>{len(all_stations)}</td>'''

for column in list_rf_row:
    html += f'''<td class=xl6621890 style='border-top:none;border-left:none'>{column}</td>'''

# для СНГ

for ugms,stations in sorted(ugm_cng.items()):
    ugms_sum = [[],[],[],[],[],[],[],[],[],[],[],[],[]]
    for index in sorted(stations,key=lambda x:index_name_cng[x]):
        html += f'''
 <tr height=25 style='height:18.75pt'>
  <td height=25 class=xl6921853 style='height:18.75pt;border-top:none'>{index_name_cng[index]}<span
  style='mso-spacerun:yes'>               </span></td>
'''

        if index in dict_cng:
            mp3_pak = dict_cng[index][3].pop('058',0) + dict_cng[index][3].pop('089',0)
            mp3_3mk = dict_cng[index][3].pop('162',0)
            mp3_h1 = dict_cng[index][3].pop('119',0)
            ak2_2m = dict_cng[index][3].pop('090',0)
            p3m_2 = dict_cng[index][3].get('068',0) + dict_cng[index][3].pop('069',0)
            u_2012 = dict_cng[index][3].get('153',0) + dict_cng[index][3].pop('160',0)
            mistake_cod = sum(dict_cng[index][3].values())
            one = dict_cng[index][4].pop('1',0)
            six = dict_cng[index][4].pop('6',0)
            seven = dict_cng[index][4].pop('7',0)
            eight = dict_cng[index][4].pop('8',0)
            fortin = dict_cng[index][4].pop('14',0)
            other = sum(dict_cng[index][4].values())

            list_one_row = [dict_cng[index][0],dict_cng[index][1],dict_cng[index][2],mp3_pak,mp3_3mk,mp3_h1,ak2_2m,p3m_2,u_2012,mistake_cod,one,six,seven,eight,fortin,other]

            [ugms_sum[i].append(zond) for i,zond in enumerate((mp3_pak,mp3_3mk,mp3_h1,ak2_2m,p3m_2,u_2012,mistake_cod,one,six,seven,eight,fortin,other))]

            for  column in list_one_row:
                html += f"<td class=xl6421853 style='border-top:none;border-left:none'>{column}</td>"
        else:
            for _ in range(16):
                html += f"<td class=xl6421853 style='border-top:none;border-left:none'>0</td>"
        html += '</tr>'

    sum_h_ugms = sum([dict_cng[index][0] for index in stations if index in dict_cng])
    sum_plan = round(sum_h_ugms/(len_month*2*len(stations)) * 100,2)
    h =[dict_cng[index][2] for index in stations if index in dict_cng]
    midl_h = str(sum(h)// len(h)) if len(h) else 0
    list_ugms_row = [sum_h_ugms,sum_plan,midl_h,sum(ugms_sum[0]),sum(ugms_sum[1]),sum(ugms_sum[2]),sum(ugms_sum[3]),sum(ugms_sum[4]),sum(ugms_sum[5]),sum(ugms_sum[6]),sum(ugms_sum[7]),sum(ugms_sum[8]),sum(ugms_sum[9]),sum(ugms_sum[10]),sum(ugms_sum[11]),sum(ugms_sum[12])]

    html += f'''<tr height=25 style='height:18.75pt'>
  <td height=25 class=xl6621853 style='height:18.75pt;border-top:none'>{ugms}/{len(stations)}</td>'''
    for column in list_ugms_row:
        html += f'''<td class=xl6621853 style='border-top:none;border-left:none'>{column}</td>'''
    html += '</tr>'


html += ''' </tr>
 <tr height=25 style='height:18.75pt'>
  <td height=25 class=xl6321853 style='height:18.75pt'></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
 </tr>
 <tr height=25 style='height:18.75pt'>
  <td height=25 class=xl6321853 style='height:18.75pt'></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
 </tr>
 <tr height=25 style='height:18.75pt'>
  <td colspan=2 height=25 class=xl6321853 style='height:18.75pt'>Причины
  окончания выпусков:</td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
 </tr>
 <tr height=25 style='height:18.75pt'>
  <td height=25 class=xl6321853 style='height:18.75pt'></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
 </tr>
 <tr height=25 style='height:18.75pt'>
  <td colspan=3 height=25 class=xl6721853 style='height:18.75pt'>&quot;1&quot;
  - разрыв оболочки</td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
 </tr>
 <tr height=25 style='height:18.75pt'>
  <td height=25 class=xl6721853 colspan=2 style='height:18.75pt'>&quot;6&quot;
  - отказ наземного оборудования</td>
  <td class=xl6721853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
 </tr>
 <tr height=25 style='height:18.75pt'>
  <td colspan=3 height=25 class=xl6721853 style='height:18.75pt'>&quot;7&quot;
  - радиопомехи</td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
 </tr>
 <tr height=25 style='height:18.75pt'>
  <td colspan=3 height=25 class=xl6721853 style='height:18.75pt'>&quot;8&quot;
  - отказ радиозонда</td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
 </tr>
 <tr height=25 style='height:18.75pt'>
  <td colspan=3 height=25 class=xl6721853 style='height:18.75pt'>&quot;14&quot;
  - пропал сигнал</td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
  <td class=xl6321853></td>
 </tr>
 <![if supportMisalignedColumns]>
 <tr height=0 style='display:none'>
  <td width=201 style='width:151pt'></td>
  <td width=71 style='width:53pt'></td>
  <td width=71 style='width:53pt'></td>
  <td width=103 style='width:77pt'></td>
  <td width=77 style='width:58pt'></td>
  <td width=77 style='width:58pt'></td>
  <td width=77 style='width:58pt'></td>
  <td width=77 style='width:58pt'></td>
  <td width=77 style='width:58pt'></td>
  <td width=77 style='width:58pt'></td>
  <td width=90 style='width:68pt'></td>
  <td width=64 style='width:48pt'></td>
  <td width=64 style='width:48pt'></td>
  <td width=64 style='width:48pt'></td>
  <td width=64 style='width:48pt'></td>
  <td width=64 style='width:48pt'></td>
  <td width=64 style='width:48pt'></td>
 </tr>
 <![endif]>
</table>

</div>


<!----------------------------->
<!--КОНЕЦ ФРАГМЕНТА ПУБЛИКАЦИИ МАСТЕРА ВЕБ-СТРАНИЦ EXCEL-->
<!----------------------------->
</body>

</html>
'''




save_report(html, file_name='html',now=now,month_now=month_now)


try:
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server,username=name,password=password, port=port)

    ftp = ssh.open_sftp()
    ftp.chdir('/home/monitor/www/monitor/2020')
    folder_month_now = f'{month_now:02}'
    if folder_month_now not in ftp.listdir():
        ftp.mkdir(folder_month_now)
    ftp.chdir(folder_month_now)
    ftp.put(f'/home/bufr/reports/report_{month_now:02d}{now.year}/{now.year}{now.month:02d}.html',f'{now.year}{now.month:02d}.html')
except:
    pass
