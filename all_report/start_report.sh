#!/bin/bash




cd /home/bufr/bufr_work/telegram_BUFR/all_report
python3 get_all_report.py && echo $(date +"%Y-%m-%d %H:%M") - create_reports >> ../start_script.log



# задача для crontab -e
#10 6 * * * /home/bufr/bufr_work/telegram_BUFR/all_report/start_report.sh

