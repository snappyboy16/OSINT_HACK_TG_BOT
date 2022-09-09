import sqlite3

sql_db = sqlite3.connect('database/db_phone.db')
cur = sql_db.cursor()


def add_phone(user_id, username, phone, region, operator, type_phone, view, status):
    cur.execute(
        'INSERT INTO phone (user_id, username, phone, region, operator, type_phone, view, status) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',(user_id, username, phone, region, operator, type_phone, view, status))
    sql_db.commit()


def add_site(user_id, username, link, name, reg, domain_reg, domain_finish, web_archive, type_site, view, status):
    cur.execute('INSERT INTO site (user_id, username, link, name, reg, domain_reg, domain_finish, web_archive,'
                ' type_site, view, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (user_id, username, link, name, reg, domain_reg, domain_finish, web_archive, type_site, view, status))
    sql_db.commit()


def set_confirm_add_phone(confirm, phone):
    cur.execute('UPDATE phone SET status = ? WHERE phone = ?', (confirm, phone))
    sql_db.commit()


def delete_add_phone(phone):
    cur.execute('DELETE FROM phone WHERE phone = ?', (phone,))
    sql_db.commit()


def set_confirm_add_site(confirm, name):
    cur.execute('UPDATE site SET confirm = ? WHERE name = ?', (confirm, name))
    sql_db.commit()


def delete_add_site(name):
    cur.execute('DELETE FROM site WHERE name = ?', (name,))
    sql_db.commit()