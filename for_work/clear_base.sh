sudo mysql < drop_base.sql
if [[ $? = 0 ]]
then
echo 'create new base CAO2'
else
echo 'can not create base CAO2'
fi

