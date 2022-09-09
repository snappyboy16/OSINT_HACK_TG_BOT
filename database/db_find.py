import sqlite3

sql_db = sqlite3.connect('database/db_phone.db')
cur = sql_db.cursor()


def find_phone_user_id(phone):
    global f_phone_user_id
    cur.execute('SELECT * FROM phone WHERE phone = ?', (phone,))
    f_phone_user_id = cur.fetchall()
    for row in f_phone_user_id:
        f_phone_user_id = row[1]
    return f_phone_user_id


def find_phone_user(phone):
    global f_phone_user
    cur.execute('SELECT * FROM phone WHERE phone = ?', (phone,))
    f_phone_user = cur.fetchall()
    for row in f_phone_user:
        f_phone_user = row[2]
    return f_phone_user


def find_phone_num(phone):
    global f_phone_num
    cur.execute('SELECT * FROM phone WHERE phone = ?', (phone,))
    f_phone_num = cur.fetchall()
    for row in f_phone_num:
        f_phone_num = row[3]
    return f_phone_num


def find_phone_reg(phone):
    global f_phone_reg
    cur.execute('SELECT * FROM phone WHERE phone = ?', (phone,))
    f_phone_reg = cur.fetchall()
    for row in f_phone_reg:
        f_phone_reg = row[4]
    return f_phone_reg


def find_phone_oper(phone):
    global f_phone_oper
    cur.execute('SELECT * FROM phone WHERE phone = ?', (phone,))
    f_phone_oper = cur.fetchall()
    for row in f_phone_oper:
        f_phone_oper = row[5]
    return f_phone_oper


def find_phone_type(phone):
    global f_phone_type
    cur.execute('SELECT * FROM phone WHERE phone = ?', (phone,))
    f_phone_type = cur.fetchall()
    for row in f_phone_type:
        f_phone_type = row[6]
    return f_phone_type


def find_phone_view(phone):
    global f_phone_view
    cur.execute('SELECT * FROM phone WHERE phone = ?', (phone,))
    f_phone_view = cur.fetchall()
    for row in f_phone_view:
        f_phone_view = row[7]
    return f_phone_view


def set_find_phone_view(view, phone):
    cur.execute('UPDATE phone SET view = view + ? WHERE phone = ?', (view, phone))
    sql_db.commit()


def find_site_user_id(name):
    cur.execute('SELECT * FROM site WHERE name = ?', (name,))
    f_site_user_id = cur.fetchall()
    for row in f_site_user_id:
        f_site_user_id = row[1]
        return f_site_user_id


def find_site_user(name):
    cur.execute('SELECT * FROM site WHERE name = ?', (name,))
    f_site_user = cur.fetchall()
    for row in f_site_user:
        f_site_user = row[2]
        return f_site_user
    

def find_site_link(name):
    cur.execute('SELECT * FROM site', (name,))
    f_site_link = cur.fetchall()
    for row in f_site_link:
        f_site_link = row[3]
        return f_site_link


def find_site_name():
    cur.execute('SELECT * FROM site')
    f_site_name = cur.fetchall()
    for row in f_site_name:
        f_site_name = row[4]
        return f_site_name


def find_site_registartor(name):
    cur.execute('SELECT * FROM site WHERE name = ?', (name,))
    f_site_registartor = cur.fetchall()
    for row in f_site_registartor:
        f_site_registartor = row[5]
        return f_site_registartor


def find_site_domain_reg(name):
    cur.execute('SELECT * FROM site WHERE name = ?', (name,))
    f_site_domain_reg = cur.fetchall()
    for row in f_site_domain_reg:
        f_site_domain_reg = row[6]
        return f_site_domain_reg


def find_site_domain_finish(name):
    cur.execute('SELECT * FROM site WHERE name = ?', (name,))
    f_site_domain_finish = cur.fetchall()
    for row in f_site_domain_finish:
        f_site_domain_finish = row[7]
        return f_site_domain_finish


def find_site_web_archive(name):
    cur.execute('SELECT * FROM site WHERE name = ?', (name,))
    f_site_web_archive = cur.fetchall()
    for row in f_site_web_archive:
        f_site_web_archive = row[8]
        return f_site_web_archive


def find_site_type(name):
    cur.execute('SELECT * FROM site WHERE name = ?', (name,))
    f_site_type = cur.fetchall()
    for row in f_site_type:
        f_site_type = row[9]
        return f_site_type


def find_site_view(name):
    cur.execute('SELECT * FROM site WHERE name = ?', (name,))
    f_site_view = cur.fetchall()
    for row in f_site_view:
        f_site_view = row[10]
        return f_site_view


def set_find_site_view(view, name):
    cur.execute('UPDATE site SET view = view + ? WHERE name = ?', (view, name))
    sql_db.commit()
