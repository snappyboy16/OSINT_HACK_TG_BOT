import sqlite3

sql_db = sqlite3.connect('database/db_phone.db')
cur = sql_db.cursor()


def set_wallet_sber(sber, user_id):
    cur.execute('UPDATE users SET sber = ? WHERE user_id = ?', (sber, user_id))
    sql_db.commit()


def set_wallet_tinkoff(tinkoff, user_id):
    cur.execute('UPDATE users SET tinkoff = ? WHERE user_id = ?', (tinkoff, user_id))
    sql_db.commit()

