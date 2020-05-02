mysqldump -u fol -pQq123456 cao_bufr_v2 > $(date "+%d-%m-%Y_%H:%M:%S")--dump_CAO.sql
if [[ $? = 0 ]]
then
echo 'backup doing'
else
echo 'backup NOTDOING'
fi
