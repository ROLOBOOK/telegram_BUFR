import os,sys, subprocess
sys.path.insert(1, '../')
from for_work.email import send_email



scripts_in_folder = [script for script in os.listdir() if script.endswith("py") and not script.startswith("get_all_report")]

err = []

one_arg = ''
if len(sys.argv) == 2:
    one_arg = sys.argv[1]
for script in scripts_in_folder:
    os.system(f'python3 {script} {one_arg}')
    errors = subprocess.Popen(['python3', script],stderr=subprocess.PIPE)
    output_er = errors.stderr.read()
    err.append(f'{script}: {output_er if len(output_er) > 1 else "OK"}')
send_email(body='\n\n'.join(err),subject="Все отчеты обновлены")
