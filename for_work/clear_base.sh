sudo mysql < del_add_base.sql
if [[ $? = 0 ]]
then
echo 'create new base CAO'
else
echo 'can not create base CAO'
fi

cd ..
python3 add_new_station_in_base.py
if [[ $? = 0 ]]
then
echo 'index_stations in base'
else
echo 'index_stations not in baseO'
fi
