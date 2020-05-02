#!/bin/bash




cd /home/bufr/bufr_work/telegram_BUFR/
python3 processing_for_cron.py && python3 get_report.py

# задача для крон запуск в 3:12 каждый день
#crontab -e
#12 3 * * * /home/bufr/bufr_work/telegram_BUFR/start_decrypt.sh
