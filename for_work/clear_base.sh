sudo mysql < del_add_base.sql
if [[ $? = 0 ]]
then
echo 'create new base CAO'
else
echo 'can not create base CAO'
fi

