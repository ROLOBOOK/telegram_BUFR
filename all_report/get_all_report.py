import os,sys
sys.path.insert(1, '../')
from for_work.email import send_email



scripts_in_folder = [script for script in os.listdir() if script.endswith("py") and not script.startswith("get_all_report")]

one_arg = ''
if len(sys.argv) == 2:
    one_arg = sys.argv[1]
for script in scripts_in_folder:
    os.system(f'python3 {script} {one_arg}')


send_email(subject="Все отчеты обновлены")
