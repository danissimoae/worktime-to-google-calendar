from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import datetime
import os.path
from sys import argv

import sqlite3
import pandas as pd
import re
from dateutil import parser


# Адрес для аутентификации
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Занести ТОКЕН календаря
CALENDAR_ID = ''
# Временной-пояс
TIMEZONE = 'Asia/Yekaterinburg'


def main():
    '''
    Основная функция. Выводит на экран последние 10 событий из календаря.
    '''
    creds = None
    # Токен json хранит токены доступа пользователя
    # и обновления и создается автоматически при первом
    # завершении процесса авторизации.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Проверка на наличие / валидность данных для входа
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Сохранение данных для следующего запуска
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # При помощи библиотеки argv получаем позиционные аргументы из запроса в терминал.
    # В зависимости от запроса запускаем нужную функцию.   
    if argv[1] == 'add':
        duration = argv[2]
        description = argv[3]
        addEvent(creds, duration, description)
    if argv[1] == 'commit':
        commitHours(creds)
    if argv[1] == 'convertdb':
        convertdb()
    if argv[1] == 'search':
        name_pattern = argv[2]
        search_database(name_pattern)


def commitHours(creds):
    '''
    Функция которая добавляет данные в БД.
    '''
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Вызов API календаря.
        today = datetime.date.today()
        timeStart = str(today) + "T00:00:00Z"
        timeEnd = str(today) + "T23:59:59Z" # 'Z' означает UTC.
        print("Получение событий о сегодняшней деятельности...")
        events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=timeStart, timeMax=timeEnd, singleEvents=True, orderBy='startTime', timeZone=TIMEZONE).execute()
        events = events_result.get('items', [])

        if not events:
            print('Нет запланированных событий.')
            return

        total_duration = datetime.timedelta(seconds=0, minutes=0, hours=0)
        id = 0
        print("Часы работы: ")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))

            # Изменение стартового времени в формат datetime.
            start_formatted = parser.isoparse(start)
            # Изменение конечного времени в формат datetime. 
            end_formatted = parser.isoparse(end) 
            duration = end_formatted - start_formatted

            total_duration += duration
            print(f"{event['summary']}, duration: {duration}")
        print(f"Все время событий: {total_duration}")

        conn = sqlite3.connect('hours.db')
        cur = conn.cursor()
        print("БД успешно открыта.")
        date = datetime.date.today()

        formatted_total_duration = total_duration.seconds/60/60
        coding_hours = (date, 'События', formatted_total_duration) 
        cur.execute("INSERT INTO hours VALUES(?, ?, ?);", coding_hours)
        conn.commit()
        print("Время всех событий успешно добавлено в БД.")

    except HttpError as error:
        print('Возникла ошибка: %s' % error)


# Добавление события в календарь.
def addEvent(creds, duration, description):
    '''
    Функция добавляет в календарь событие, начинающиеся сразу после обращения.
    '''
    start = datetime.datetime.utcnow()
    
    end = datetime.datetime.utcnow() + datetime.timedelta(hours=int(duration))
    start_formatted = start.isoformat() + 'Z'
    end_formatted = end.isoformat() + 'Z'

    event = {
    'summary': description,
    'start': {
        'dateTime': start_formatted,
        'timeZone': TIMEZONE,
        },
    'end': {
        'dateTime': end_formatted,
        'timeZone': TIMEZONE,
        },
    }

    service = build('calendar', 'v3', credentials=creds)
    event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    print('Событие создано: %s' % (event.get('htmlLink')))


def getHours(number_of_days):
    '''
    Функция, принимает количество последних дней и возвращает данные о событиях
    за эти дни.
    '''
    # Получение текущей даты.
    today = datetime.date.today()
    seven_days_ago = today + datetime.timedelta(days=-int(number_of_days))

    # Получение времени из БД.
    conn = sqlite3.connect('hours.db')
    cur = conn.cursor()

    cur.execute(f"SELECT DATE, HOURS FROM hours WHERE DATE between ? AND ?", (seven_days_ago, today))

    hours = cur.fetchall()

    total_hours = 0
    for element in hours:
        print(f"{element[0]}: {element[1]}")
        total_hours += element[1]
    print(f"Total hours: {total_hours}")
    print(f"Average hours: {total_hours/float(number_of_days)}")


def convertdb():
    '''
    Функция конвертации БД в excel таблицу.
    '''
    try:
        # Подключение к базе данных SQLite
        conn = sqlite3.connect('hours.db')
        
        # Использование регулярного выражения для выбора всех столбцов из таблицы
        table_name = "hours"
        query = f"SELECT * FROM {table_name};"
        
        # Чтение данных из базы данных с использованием pandas
        df = pd.read_sql_query(query, conn)

        # Создание Excel-файла
        excel_file = "hours_data.xlsx"
        df.to_excel(excel_file, index=False)
        
        print(f"Данные успешно конвертированы в Excel и сохранены в файле: {excel_file}")

    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")

    finally:
        # Закрытие соединения с базой данных
        if conn:
            conn.close()


def search_database(regex_pattern):
    '''
    Функция осуществляет поиск в базе данных. Возможен поиск по дате.
    '''
    try:
        # Подключение к базе данных
        connection = sqlite3.connect('hours.db')
        cursor = connection.cursor()

        # Выполнение запроса к базе данных
        query = f"SELECT * FROM hours"
        cursor.execute(query)

        # Получение результатов запроса
        rows = cursor.fetchall()

        # Фильтрация результатов с использованием регулярного выражения
        result_rows = [row for row in rows if any(re.search(regex_pattern, str(cell)) for cell in row)]

        # Вывод строк с совпадениями
        for row in result_rows:
            print(row)

        connection.close()
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == '__main__':
    main()


    