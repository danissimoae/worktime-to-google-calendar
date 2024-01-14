import sqlite3

conn = sqlite3.connect(f'hours.db')
cur = conn.cursor()
print("База данных успешно открыта.")


conn.execute('''CREATE TABLE hours
        (DATE       DATE    NOT NULL,
        CATEGORY           TEXT    NOT NULL,
        HOURS            INT     NOT NULL);''')
print("База данных успешно создана.")