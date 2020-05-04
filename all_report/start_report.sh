#!/bin/bash




cd /home/bufr/bufr_work/telegram_BUFR/all_report
python3 count_pusk.py


# задача для crontab -e
#10 6 * * * /home/bufr/bufr_work/telegram_BUFR/all_report/start_report.sh

