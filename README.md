# telegram_BUFR
обработка аэрологический телеграмм
1. получаем из закодированых телеграмм информацию об типах использованых радиозондах и составляем файл отчет

установка
в папке for_work запустить файл install_pip3_and_pybufrkit.sh. Мы устанавливаем pip3  и библиотеку pybufrkit

Запуск
В папку со скриптом копируем/вставляем телеграммы, которые нужно обработать.
Запускаем скрипт на питоне, в терминале, в папке со скриптом пишем команду: python3 check_Zonde.py
После работы скрипта, проверенные файлы будут лежать в папке check_telegram, файлы с ошибками в папке file_with_mistake, в папке со скриптом появится файл "отчет по радиозондам за месяц".

Время работы скрипта зависит от количества файлов.