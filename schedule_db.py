import sqlite3

from datetime import datetime, timedelta

date1 = datetime.now()
date2 = date1 + timedelta(hours=1)
full_dt_format: str = '%d.%m.%Y %H:%M:%S'


dates = (
    {"datetime_start": date1.strftime(full_dt_format), "datetime_end": date2.strftime(full_dt_format)}
)

path = '/home/churakov/dev/dbs/dbsqlite_telegrambot/tg_test'

with sqlite3.connect(database=path) as conn:
    cursor = conn.cursor()
    cursor.execute("""
        insert into lessons(datetime_start, datetime_end)
        values (:datetime_start, :datetime_end)
    """, dates)
    conn.commit()