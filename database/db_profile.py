import sqlite3

sql_db = sqlite3.connect('database/db_phone.db')
cur = sql_db.cursor()


def add_users(user_id, name, username, money, view, viewed_phone, viewed_site):
    cur.execute('INSERT INTO users (user_id, name, username, money, view, viewed_phone, viewed_site) '
                'VALUES (?, ?, ?, ?, ?, ?, ?)', (user_id, name, username, view, money, viewed_phone, viewed_site))
    sql_db.commit()


def profile_id(user_id):
    cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    p_id = cur.fetchall()
    for row in p_id:
        pid = row[0]
        return pid


def profile_money(user_id):
    cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    p_money = cur.fetchall()
    for row in p_money:
        money = float(row[4])
        return money


def profile_money_hold(user_id):
    cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    p_money_hold = cur.fetchall()
    for row in p_money_hold:
        money_hold = float(row[5])
        return money_hold


def profile_money_withdraw(user_id):
    cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    p_money_withdraw = cur.fetchall()
    for row in p_money_withdraw:
        money_withdraw = float(row[6])
        return money_withdraw


def profile_money_sber(user_id):
    cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    p_money_sber = cur.fetchall()
    for row in p_money_sber:
        money_sber = str(row[7])
        return money_sber


def profile_money_tinkoff(user_id):
    cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    p_money_tinkoff = cur.fetchall()
    for row in p_money_tinkoff:
        money_tinkoff = str(row[8])
        return money_tinkoff


def profile_view(user_id):
    cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    p_view = cur.fetchall()
    for row in p_view:
        view = str(row[9])
        return view


def profile_viewed_phone(user_id):
    cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    p_viewed_phone = cur.fetchall()
    for row in p_viewed_phone:
        viewed_phone = str(row[10])
        return viewed_phone


def profile_viewed_site(user_id):
    cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    p_viewed_site = cur.fetchall()
    for row in p_viewed_site:
        viewed_site = str(row[11])
        return viewed_site


def profile_phone(user_id):
    cur.execute('SELECT * FROM phone WHERE user_id = ? LIMIT 10', (user_id,))
    p_phone = cur.fetchall()
    return '\n\n'.join(' | '.join(['📱 +' + (str(row[3])), '⚠️ ' + str(row[6]), '👁 ' + str(row[7])])
                       for row in p_phone)


def profile_phone_count(user_id):
    cur.execute('SELECT COUNT(*) FROM phone WHERE user_id = ?', (user_id,))
    p_phone_count = cur.fetchall()
    return p_phone_count


def profile_site(user_id):
    cur.execute('SELECT * FROM site WHERE user_id = ? LIMIT 10', (user_id,))
    p_site = cur.fetchall()
    return '\n\n'.join(' | '.join(['🔗 ' + str(row[4]), '⚠️ ' + str(row[9]), '👁 ' + str(row[10])])
                       for row in p_site)


def profile_site_count(user_id):
    cur.execute('SELECT COUNT(*) FROM site WHERE user_id = ?', (user_id,))
    p_phone_count = cur.fetchall()
    return p_phone_count


def set_profile_view(view, user_id):
    cur.execute('UPDATE users SET view = view + ? WHERE user_id = ?', (view, user_id))
    sql_db.commit()


def set_profile_viewed_phone(viewed_phone, user_id):
    cur.execute('UPDATE users SET viewed_phone = viewed_phone + ? WHERE user_id = ?', (viewed_phone, user_id,))
    sql_db.commit()


def set_profile_viewed_site(viewed_site, user_id):
    cur.execute('UPDATE users SET viewed_site = viewed_site + ? WHERE user_id = ?', (viewed_site, user_id,))
    sql_db.commit()


def set_profile_money_hold(money_hold, user_id):
    cur.execute('UPDATE users SET money_hold = money_hold + ? WHERE user_id = ?', (money_hold, user_id))
    sql_db.commit()


def set_profile_minus_money_hold(money_hold, user_id):
    cur.execute('UPDATE users SET money_hold = money_hold - ? WHERE user_id = ?', (money_hold, user_id))
    sql_db.commit()


def set_profile_money(money, user_id):
    cur.execute('UPDATE users SET money = money + ? WHERE user_id = ?', (money, user_id))
    sql_db.commit()
