# worktime-to-google-calendar
# Python-script that sends work activity data to your Google calendar, database, Excel spreadsheet.
Python-скрипт, отправляющий данные рабочей деятельности в ваш гугл-календарь, БД, Excel-таблицу.

### Installation
Installing the necessary libraries:

### Установка
Установка необходимых библиотек:

`pip install pandas`

`pip install google-auth-oauthlib`

`pip install google-api-python-client`

`pip install python-dateutil`


### Customization
To start writing a program, you need to get a JSON token from Google. This is done on the Google API page (https://console.cloud.google.com/apis/credentials/consent?project=claendarapi&pli=1).

After that, you need to download the JSON token and copy it to the project folder.

You will also need a unique identifier of the calendar in which the work will be recorded. This is done on the Google Calendar page.

In ``main.py ``enter your token in the variable `CALENDAR_ID`, in the variable `TIMEZONE` select your time zone in the format `Asia/Yekaterinburg`


### Настройка
Для начала написания программы необходимо получить JSON-токен от Google. Делается это на странице GoogleAPI (https://console.cloud.google.com/apis/credentials/consent?project=claendarapi&pli=1).

После необходимо скачать JSON-токен и скопировать его в папку с проектом.

Также, понадобится уникальный идентификатор календаря, в который будут вноситься учет работы. Делается это на странице Google Calendar.

В ```main.py``` в переменную `CALENDAR_ID` занести ваш токен, в переменной `TIMEZONE` выберите ваш часовой пояс в формате `Asia/Yekaterinburg`.


### Commands
It is necessary to run `main.py ` and `createTable.py ` (`createTable.py `only once to create a database). After that, the program provides the following functions that are performed after entering commands into the terminal:
- Authorization and adding an event:
`python main.py ad <duration_in_hours> "<event_description>"`
Here `<duration_in_hours>` is the desired duration of the event in hours, and <event_description> is the description of the event.
- Recording hours worked in the database:
`python main.py commit`
- Getting clock data for the last `N` days:
`python main.py getHours <number_of_days>`
Where `<number_of_days>` is the number of recent days for which you want to receive data.
The first time you run the program, you need to create a database using a script `createTable.py `. Inside it, a connection is established to the SQLite3 database built into python.


### Команды
Необходимо запустить `main.py` и `createTable.py` (`createTable.py` лишь один раз для создания базы данных). После программа предоставляет следующие функции, выполняющиеся после ввода команд в терминал:
- Авторизация и добавление события:
`python main.py add <duration_in_hours> "<event_description>"`
Здесь `<duration_in_hours>` - желаемая продолжительность события в часах, а <event_description> - описание события.
- Запись отработанных часов в базу данных:
`python main.py commit`
- Получение данных о часах за последние `N` дней:
`python main.py getHours <number_of_days>`
Где `<number_of_days>` - количество последних дней, за которые вы хотите получить данные.
При первом запуске программы необходимо создать базу данных с помощью скрипта `createTable.py`. Внутри него происходит установка подключения к базе данных SQLite3, встроенной в python. 
