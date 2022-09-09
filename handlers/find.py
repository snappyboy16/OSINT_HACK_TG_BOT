import sqlite3
from time import sleep
from aiogram.types import InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from start_bot import dp, bot
from database import db_find, db_profile
from keyboards import user_kb

sql_db = sqlite3.connect('database/db_phone.db')
cur = sql_db.cursor()


def phone_num_exist(phone):
    cur.execute('SELECT * FROM phone WHERE phone = ?', (phone,))
    phone_ex = cur.fetchall()
    return bool(len(phone_ex))


def site_name_exist(name):
    cur.execute('SELECT * FROM site WHERE name = ?', (name,))
    site_ex = cur.fetchall()
    return bool(len(site_ex))


class UserFind(StatesGroup):
    mess = State()


@dp.callback_query_handler(text='check')
async def menu_find(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, 'Введите номер или ссылку на сайт')
    await UserFind.mess.set()


@dp.message_handler(state=UserFind.mess)
async def find_mess(message: types.Message, state: FSMContext):
    global user_mess
    user_mess = message.text
    if '+' in user_mess:
        phone_mess = user_mess[1:]
        phone_user_id = db_find.find_phone_user_id(phone_mess)
        phone_user = db_find.find_phone_user(phone_mess)
        phone_num = db_find.find_phone_num(phone_mess)
        phone_reg = db_find.find_phone_reg(phone_mess)
        phone_oper = db_find.find_phone_oper(phone_mess)
        phone_type = db_find.find_phone_type(phone_mess)
        phone_view = db_find.find_phone_view(phone_mess)
        if len(phone_mess) == 11:
            if phone_mess.isdigit():
                if not phone_num_exist(phone=phone_mess):
                    await bot.send_message(message.from_user.id, 'Номер отсутсвует в базе')
                    await state.finish()
                else:
                    await bot.send_message(message.from_user.id, '🔎 Собираю информацию о номере...')
                    sleep(1)
                    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1,
                                                text='📞 Проверяю номер...')
                    sleep(1)
                    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1,
                                                text='🎉 Готово')
                    sleep(1)
                    db_profile.set_profile_viewed_phone(1, message.from_user.id)
                    db_profile.set_profile_view(1, phone_user_id)
                    db_find.set_find_phone_view(1, phone_num)
                    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text=
                                                f'📱 <b>Номер:</b> +{phone_num}\n\n'
                                                f'🏙 <b>Регион:</b> {phone_reg}\n\n'
                                                f'🏢 <b>Оператор:</b> {phone_oper}\n\n'
                                                f'⚠️<b> Вид номера:</b> {phone_type}\n\n'
                                                f'👁 <b> Просмотров: </b>{phone_view}\n\n'
                                                f'👤 <b> Добавлен:</b> @{phone_user}\n\n'
                                                f'', parse_mode='HTML', reply_markup=user_kb.start_menu_kb)
                    await state.finish()
            else:
                await bot.send_message(message.from_user.id, 'Введите номер а не текст, попробуйте ещё раз',
                                       reply_markup=user_kb.start_menu_kb)
                await state.finish()
        else:
            await bot.send_message(message.from_user.id, 'Номер введён не правильно, попробуйте ещё раз',
                                   reply_markup=user_kb.start_menu_kb)
            await state.finish()
    elif 'http://' in user_mess or 'https://' in user_mess:
        site_link = user_mess
        sep_site = 'https://' or 'http://'
        site_link_clear = site_link.replace(sep_site, '')
        if not '/' in site_link_clear:
            if not site_name_exist(name=site_link_clear):
                await bot.send_message(message.from_user.id, 'Сайта нет в базе')
                await state.finish()
            else:
                site_user_id = db_find.find_site_user_id(site_link_clear)
                site_user = db_find.find_site_user(site_link_clear)
                site_registrator = db_find.find_site_registartor(site_link_clear)
                site_domain_reg = db_find.find_site_domain_reg(site_link_clear)
                site_domain_finish = db_find.find_site_domain_finish(site_link_clear)
                site_web_archive = db_find.find_site_web_archive(site_link_clear)
                site_type = db_find.find_site_type(site_link_clear)
                site_view = db_find.find_site_view(site_link_clear)

                web_kb = InlineKeyboardMarkup(row_width=1)
                web_archive = InlineKeyboardButton('📁 Web-Archive', url=site_web_archive)
                menu = InlineKeyboardButton('🏠 Меню', callback_data='menu')
                web_kb.row(web_archive).row(menu)

                db_profile.set_profile_viewed_site(1, message.from_user.id)
                db_profile.set_profile_view(1, site_user_id)
                db_find.set_find_site_view(1, site_link_clear)
                await bot.send_message(message.from_user.id, f'📝 <b>Имя: </b>{site_link_clear}\n\n'
                                                             f'🌐 <b>Регистратор: </b>{site_registrator}\n\n'
                                                             f'📅 <b>Домен создан: </b>{site_domain_reg}\n\n'
                                                             f'🗓 <b>Срок домена: </b>{site_domain_finish}\n\n'
                                                             f'⚠️ <b>Вид сайта: </b>{site_type}\n\n'
                                                             f'👁 <b>Просмотры: </b>{site_view}\n\n'
                                                             f'👤 <b>Добавлен: </b>@{site_user}', reply_markup=web_kb,
                                       disable_web_page_preview=True, parse_mode='HTML')
                await state.finish()
        else:
            site_link_db = site_link_clear[0:site_link_clear.index('/')]
            if not site_name_exist(name=site_link_db):
                await bot.send_message(message.from_user.id, 'Сайта нет в базе')
                await state.finish()
            else:
                site_user_id = db_find.find_site_user_id(site_link_db)
                site_user = db_find.find_site_user(site_link_db)
                site_registrator = db_find.find_site_registartor(site_link_db)
                site_domain_reg = db_find.find_site_domain_reg(site_link_db)
                site_domain_finish = db_find.find_site_domain_finish(site_link_db)
                site_web_archive = db_find.find_site_web_archive(site_link_db)
                site_type = db_find.find_site_type(site_link_db)
                site_view = db_find.find_site_view(site_link_db)

                web_kb = InlineKeyboardMarkup(row_width=1)
                web_archive = InlineKeyboardButton('📁 Web-Archive', url=site_web_archive)
                menu = InlineKeyboardButton('🏠 Меню', callback_data='menu')
                web_kb.row(web_archive).row(menu)

                db_profile.set_profile_viewed_site(1, message.from_user.id)
                db_profile.set_profile_view(1, site_user_id)
                db_find.set_find_site_view(1, site_link_db)
                await bot.send_message(message.from_user.id, f'📝 <b>Имя: </b>{site_link_db}\n\n'
                                                             f'🌐 <b>Регистратор: </b>{site_registrator}\n\n'
                                                             f'📅 <b>Домен создан: </b>{site_domain_reg}\n\n'
                                                             f'🗓 <b>Срок домена: </b>{site_domain_finish}\n\n'
                                                             f'⚠️ <b>Вид сайта: </b>{site_type}\n\n'
                                                             f'👁 <b>Просмотры: </b>{site_view}\n\n'
                                                             f'👤 <b>Добавлен: </b>@{site_user}', reply_markup=web_kb,
                                       disable_web_page_preview=True, parse_mode='HTML')
                await state.finish()
    else:
        await bot.send_message(message.from_user.id, 'Я тебя не понимаю')
        await state.finish()


def register_handlers_find(dp: Dispatcher):
    dp.register_message_handler(menu_find, text='check')
    dp.register_message_handler(find_mess, state=UserFind.mess)
