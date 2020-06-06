#!/bin/bash




cd /home/bufr/bufr_work/telegram_BUFR/all_report
python3 count_pusk.py && python3 end_h_pusk.py  && python3 nomer_pusk.py && python3 pusk_repit.py  && python3 reason_end.py && python3 type_r-z.py && python3 bterm.py && python3 bstat.py && echo $(date +"%Y-%m-%d %H:%M") - create_reports >> ../start_script.log



# задача для crontab -e
#10 6 * * * /home/bufr/bufr_work/telegram_BUFR/all_report/start_report.sh

