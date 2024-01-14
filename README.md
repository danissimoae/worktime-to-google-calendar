# worktime-to-google-calendar
Python-скрипт, отправляющий данные рабочей деятельности в ваш гугл-календарь, БД, Excel-таблицу.

### Установка
Установка необходимых библиотек:
`pip install pandas
pip install google-auth-oauthlib
pip install google-api-python-client
pip install python-dateutil`

### Настройка
Для начала написания программы необходимо получить JSON-токен от Google. Делается это на странице GoogleAPI (https://console.cloud.google.com/apis/credentials/consent?project=claendarapi&pli=1).
После необходимо скачать JSON-токен и скопировать его в папку с проектом.
Также, понадобится уникальный идентификатор календаря, в который будут вноситься учет работы. Делается это на странице Google Calendar.
В ```main.py``` в переменную `CALENDAR_ID` занести ваш токен, в переменной `TIMEZONE` выберите ваш часовой пояс в формате `Asia/Yekaterinburg`.


### Команды
Программа предоставляет следующие команды:
- Авторизация и добавление события:
`python script.py add <duration_in_hours> "<event_description>"`
Здесь `<duration_in_hours>` - желаемая продолжительность события в часах, а <event_description> - описание события.
- Запись отработанных часов в базу данных:
`python script.py commit`
- Получение данных о часах за последние `N` дней:
`python script.py getHours <number_of_days>`
Где `<number_of_days>` - количество последних дней, за которые вы хотите получить данные.
При первом запуске программы необходимо создать базу данных с помощью скрипта `createTable.py`. Внутри него происходит установка подключения к базе данных SQLite3, встроенной в python. 
