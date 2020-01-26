mysqldump -u fol -pQq123456 cao > $(date "+%d-%m-%Y_%H:%M:%S")--dump_CAO.sql
if [[ $? = 0 ]]
then
echo 'backup doing'
else
echo 'backup NOTDOING'
fi
