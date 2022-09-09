import sqlite3

sql_db = sqlite3.connect('database/db_phone.db')
cur = sql_db.cursor()


def admin_phones():
    cur.execute('SELECT * FROM phone LIMIT 50')
    a_phone = cur.fetchall()
    return '\n\n'.join(' | '.join(['📱 +' + (str(row[3])), '⚠️ ' + str(row[6]), '👁 ' + str(row[7]), str(row[8])])
                       for row in a_phone)


def admin_phones_count():
    cur.execute('SELECT COUNT(*) FROM phone')
    a_phone_count = cur.fetchall()
    return a_phone_count


def set_status_phone(status, phone):
    cur.execute('UPDATE phone SET status = ? WHERE phone = ?', (status, phone))
    sql_db.commit()


def delete_status_phone(phone):
    cur.execute('DELETE FROM phone WHERE phone = ?', (phone,))
    sql_db.commit()


def admin_sites():
    cur.execute('SELECT * FROM site LIMIT 50')
    a_site = cur.fetchall()
    return '\n\n'.join(' | '.join(['🔗 ' + str(row[4]), '⚠️ ' + str(row[9]), '👁 ' + str(row[10]), str(row[11])])
                       for row in a_site)


def admin_sites_count():
    cur.execute('SELECT COUNT(*) FROM site')
    a_site_count = cur.fetchall()
    return a_site_count


def set_status_site(status, name):
    cur.execute('UPDATE site SET status = ? WHERE name = ?', (status, name))
    sql_db.commit()


def delete_status_site(name):
    cur.execute('DELETE FROM site WHERE name = ?', (name,))
    sql_db.commit()