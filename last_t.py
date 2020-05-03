import datetime
from  processing_bufr import *
import MySQLdb, os
from datetime import date, timedelta


c = datetime.date.today() - datetime.date(2020,1,1)
days = int(str(c).split()[0])


today = datetime.datetime.now()

for day_one in range(3,days):
    main(days=day_one)
