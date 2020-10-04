import re,os,datetime


def get_type_zonde(file):
    try:
        with open(file) as f:
            text = f.read()
    except:
        return ''

    TTBB_all = re.findall(r'TTBB [\w|/\w|/\w|/\w|/\w|/\s]*=',text)
    result = ''
    for one in TTBB_all:
        ttbb = re.findall(r'TTBB [\w|/\w|/\w|/\w|/\w|/\s]{11}',one)
        if ttbb: ttbb = ttbb[0].replace('TTBB ','')
        zond = re.findall(r'31313 [\w|/\w|/\w|/\w|/\w|/]{5}',one)
        if zond: zond = zond[0]
        if ttbb and zond:
            result  += f'{ttbb} {zond}\n'
    return result
a = '''
result = ''
path = '/home/bufr/aero_bufr/res2/KN04/2020/09/'
os.chdir(path)
folders = os.listdir()
for folder in folders:
    result += f'    Folder: {folder}\n'
    os.chdir(f'{path}/{folder}')
    files = os.listdir()
    for file in files:
        r = get_type_zonde(file)
        r = r if r else 'NOT FIND TTBB\n'
        result += f'{file}\n{r}{"#"*25}\n'
time_now = datetime.datetime.now().strftime('%d.%m.%y__%H:%M')
with open(f'/home/bufr/reports/report_KH-04/KH-04_{time_now}.txt', 'w') as f:
    f.write(result)
'''
if __name__ == "__main__":
    result = ''
    path = '/home/bufr/aero_bufr/res2/KN04/2020/09/'
    os.chdir(path)
    folders = os.listdir()
    for folder in folders:
        os.chdir(f'{path}/{folder}')
        files = os.listdir()
        for file in files:
            r = get_type_zonde(file)
            result += f'{r}'
    time_now = datetime.datetime.now().strftime('%d.%m.%y__%H:%M')
    with open(f'/home/bufr/reports/report_KH-04/KH-04_{time_now}_only_text.txt', 'w') as f:
        f.write(result)

