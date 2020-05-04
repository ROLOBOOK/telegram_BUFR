#!/bin/bash




cd /home/bufr/bufr_work/telegram_BUFR/all_report
python3 count_pusk.py && python3 end_h_pusk.py  && python3 nomer_pusk.py && python3 pusk_repit.py  && python3 reason_end.py


# задача для crontab -e
#10 6 * * * /home/bufr/bufr_work/telegram_BUFR/all_report/start_report.sh

