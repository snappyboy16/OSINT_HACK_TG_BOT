import sqlite3
from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from start_bot import dp, bot
from database import db_profile
from keyboards import user_kb, admin_kb
from config import ADMIN_ID

sql_db = sqlite3.connect('database/db_phone.db')
cur = sql_db.cursor()


def user_exist(user_id):
    cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cur.fetchall()
    return bool(len(user))


def check_channel(user_id):
    if user_id['status'] != 'left':
        return True
    else:
        return False


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    if not user_exist(user_id=message.from_user.id):
        if not message.from_user.username:
            await bot.send_message(message.from_user.id, 'Укажите в настройках свой Username')
        else:
            await bot.send_message(message.from_user.id,
                                   '👋 Приветсвую, я бот по поиску <b>мошенников</b>, '
                                   'чтобы продолжить <b>подпишись на канал</b>. '
                                   'Там будут новости про <b>будущее проекта</b>, и не только 😉',
                                   reply_markup=user_kb.check_channel_kb, parse_mode='HTML')
    else:
        if message.from_user.id == ADMIN_ID:
            await bot.send_message(message.from_user.id,
                                   '🏠 <b>Хак Скам</b> - сервис, <b>проверки</b> на мошенничество\n\n'
                                   '👁 <b>Проверить</b>\n\n'
                                   '📱 <b>Для получения информации о телефоне</b>, пришлите <b>номер телефона</b> в '
                                   'формате (<i>+79000000000</i>)\n '
                                   '🔗 <b>Для получения информации о сайте</b>, пришлите <b>ссылку на сайт</b> в '
                                   'формате (<i>https://google.ru</i>)\n\n '
                                   '➕ <b>Добавить</b>\n\n'
                                   '💰 <b>Для получения вознаграждения</b>, добавьте <b>номер мошенника</b> или '
                                   '<b>ссылку на сайт мошенника</b>',
                                   reply_markup=admin_kb.menu_kb, parse_mode='HTML')
        else:
            await bot.send_message(message.from_user.id,
                                   '🏠 <b>Хак Скам</b> - сервис, <b>проверки</b> на мошенничество\n\n'
                                   '👁 <b>Проверить</b>\n\n'
                                   '📱 <b>Для получения информации о телефоне</b>, пришлите <b>номер телефона</b> в формате (<i>+79000000000</i>)\n'
                                   '🔗 <b>Для получения информации о сайте</b>, пришлите <b>ссылку на сайт</b> в формате (<i>https://google.ru</i>)\n\n'
                                   '➕ <b>Добавить</b>\n\n'
                                   '💰 <b>Для получения вознаграждения</b>, добавьте <b>номер мошенника</b> или <b>ссылку на сайт мошенника</b>',
                                   reply_markup=user_kb.menu_kb, parse_mode='HTML')


@dp.callback_query_handler(text='check_channel')
async def sub_check_channel(call: types.CallbackQuery):
    if check_channel(await bot.get_chat_member(chat_id='@hackscamcommunity', user_id=call.from_user.id)):
        await call.message.delete()
        await bot.send_message(call.from_user.id, '🏠 <b>Хак Скам</b> - сервис, <b>проверки</b> на мошенничество\n\n'
                                                  '👁 <b>Проверить</b>\n\n'
                                                  '📱 <b>Для получения информации о телефоне</b>, пришлите <b>номер телефона</b> в формате (<i>+79000000000</i>)\n'
                                                  '🔗 <b>Для получения информации о сайте</b>, пришлите <b>ссылку на сайт</b> в формате (<i>https://google.ru</i>)\n\n'
                                                  '➕ <b>Добавить</b>\n\n'
                                                  '💰 <b>Для получения вознаграждения</b>, добавьте <b>номер мошенника</b> или <b>ссылку на сайт мошенника</b>',
                               reply_markup=user_kb.menu_kb, parse_mode='HTML')
        db_profile.add_users(call.from_user.id, call.from_user.first_name, call.from_user.username, 0, 0, 0, 0)
    else:
        await call.message.delete()
        await bot.send_message(call.from_user.id,
                               '⚠️Чтобы продолжить, <b>подпишись на канал</b> ⚠️',
                               reply_markup=user_kb.check_channel_kb, parse_mode='HTML')


@dp.callback_query_handler(text='menu')
async def menu_callback(call: types.CallbackQuery):
    await call.message.delete()
    if call.from_user.id == ADMIN_ID:
        await bot.send_message(ADMIN_ID, '🏠 <b>Хак Скам</b> - сервис, <b>проверки</b> на мошенничество\n\n'
                                                  '👁 <b>Проверить</b>\n\n'
                                                  '📱 <b>Для получения информации о телефоне</b>, пришлите <b>номер '
                                                  'телефона</b> в формате (<i>+79000000000</i>)\n '
                                                  '🔗 <b>Для получения информации о сайте</b>, пришлите <b>ссылку на '
                                                  'сайт</b> в формате (<i>https://google.ru</i>)\n\n '
                                                  '➕ <b>Добавить</b>\n\n'
                                                  '💰 <b>Для получения вознаграждения</b>, добавьте <b>номер '
                                                  'мошенника</b> или <b>ссылку на сайт мошенника</b>',
                               reply_markup=admin_kb.menu_kb, parse_mode='HTML')
    else:
        await bot.send_message(call.from_user.id, '🏠 <b>Хак Скам</b> - сервис, <b>проверки</b> на мошенничество\n\n'
                                              '👁 <b>Проверить</b>\n\n'
                                              '📱 <b>Для получения информации о телефоне</b>, пришлите <b>номер '
                                              'телефона</b> в формате (<i>+79000000000</i>)\n '
                                              '🔗 <b>Для получения информации о сайте</b>, пришлите <b>ссылку на '
                                              'сайт</b> в формате (<i>https://google.ru</i>)\n\n '
                                              '➕ <b>Добавить</b>\n\n'
                                              '💰 <b>Для получения вознаграждения</b>, добавьте <b>номер '
                                              'мошенника</b> или <b>ссылку на сайт мошенника</b>',
                           reply_markup=user_kb.menu_kb, parse_mode='HTML')


def register_handlers_main(dp: Dispatcher):
    dp.register_message_handler(start_message, commands=['start'])
    dp.register_message_handler(menu_callback, text='menu')
