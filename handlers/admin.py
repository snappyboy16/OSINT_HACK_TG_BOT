import sqlite3
from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InputFile
from start_bot import dp, bot
from database import db_admin, db_profile, db_find
from keyboards import admin_kb
from config import ADMIN_ID

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


class AdminPhones(StatesGroup):
    confirm_ph = State()
    delete_ph = State()


class AdminSites(StatesGroup):
    confirm_st = State()
    delete_st = State()


@dp.callback_query_handler(text='admin')
async def menu_admin(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(ADMIN_ID, 'Добро пожаловать в Админку Хак Скама', reply_markup=admin_kb.admin_menu_kb)


@dp.callback_query_handler(text='admin_phones')
async def menu_admin_phones(call: types.CallbackQuery):
    phones = db_admin.admin_phones()
    phones_count = db_admin.admin_phones_count().pop()[0]
    if phones_count > 50:
        with open('files/index(phones).html', 'w', encoding='utf-8') as f:
            f.write(phones)
        doc = InputFile('files/index(sites).html')
        await call.message.delete()
        await bot.send_message(ADMIN_ID, '📱 Номера собраны в файл')
        await bot.send_document(ADMIN_ID, doc)
    else:
        await call.message.delete()
        await bot.send_message(ADMIN_ID, f'📱 <b>Номера Хак Скама ({phones_count})</b>\n\n<b>{phones}</b>',
                               parse_mode='HTML', reply_markup=admin_kb.admin_menu_phones_kb)


@dp.callback_query_handler(text='confirm_phones')
async def menu_admin_confirm_phones(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(ADMIN_ID, 'Введите номер телефона')
    await AdminPhones.confirm_ph.set()


@dp.message_handler(state=AdminPhones.confirm_ph)
async def admin_confirm_phones(message: types.Message, state: FSMContext):
    phone_mess = message.text
    if len(phone_mess) == 11:
        if not phone_num_exist(phone=phone_mess):
            await bot.send_message(ADMIN_ID, 'Номера нет в базе')
        else:
            phone_user = db_find.find_phone_user_id(phone_mess)
            profile_money = float(0.2) + db_profile.profile_money(phone_user)
            db_profile.set_profile_money(profile_money, phone_user)
            db_profile.set_profile_minus_money_hold(float(0.2), phone_user)
            db_admin.set_status_phone('Подтверждено', phone_mess)
            await bot.send_message(phone_user, f'Номер {phone_mess} подтвержден!\n\nНа ваш баланс зачислено 0.2 Р.')
            await bot.send_message(ADMIN_ID, f'Номер {phone_mess} подтвержден!')
            await state.finish()
    else:
        await bot.send_message(ADMIN_ID, 'Непрвильно введен номер')
        await state.finish()


@dp.callback_query_handler(text='delete_phones')
async def menu_admin_delete_phones(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(ADMIN_ID, 'Введите номер телефона для удаления')
    await AdminPhones.delete_ph.set()


@dp.message_handler(state=AdminPhones.delete_ph)
async def admin_delete_phones(message: types.Message, state: FSMContext):
    phone_mess = message.text
    if len(phone_mess) == 11:
        if not phone_num_exist(phone=phone_mess):
            await bot.send_message(ADMIN_ID, 'Номера нет в базе')
        else:
            phone_user = db_find.find_phone_user_id(phone_mess)
            db_profile.set_profile_minus_money_hold(float(0.2), phone_user)
            db_admin.delete_status_phone(phone_mess)
            await bot.send_message(phone_user, f'Номер {phone_mess} удален!\n\nС вашего баланса списано 0.2 Р.')
            await bot.send_message(ADMIN_ID, f'Номер {phone_mess} удален!')
            await state.finish()
    else:
        await bot.send_message(ADMIN_ID, 'Неправильно введён номер')
        await state.finish()


@dp.callback_query_handler(text='admin_sites')
async def menu_admin_sites(call: types.CallbackQuery):
    sites = db_admin.admin_sites()
    sites_count = db_admin.admin_sites_count().pop()[0]
    if sites_count > 50:
        with open('files/index(sites).html', 'w', encoding='utf-8') as f:
            f.write(sites)
        doc = InputFile('files/index(sites).html')
        await call.message.delete()
        await bot.send_message(ADMIN_ID, '🔗 Сайты собраны в файл')
        await bot.send_document(ADMIN_ID, doc)
    else:
        await call.message.delete()
        await bot.send_message(ADMIN_ID, f'🔗 <b>Сайты Хак Скама ({sites_count})</b>\n\n<b>{sites}</b>',
                               parse_mode='HTML', reply_markup=admin_kb.admin_menu_sites_kb,
                               disable_web_page_preview=True)


@dp.callback_query_handler(text='confirm_sites')
async def menu_admin_confirm_sites(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(ADMIN_ID, 'Введите ссылку на сайт')
    await AdminSites.confirm_st.set()


@dp.message_handler(state=AdminSites.confirm_st)
async def admin_confirm_sites(message: types.Message, state: FSMContext):
    site_mess = message.text
    if not site_name_exist(name=site_mess):
        await bot.send_message(message.from_user.id, 'Сайта нет в базе')
        await state.finish()
    else:
        site_user = db_find.find_site_user_id(site_mess)
        profile_money = float(0.2) + db_profile.profile_money(site_user)
        db_profile.set_profile_money(profile_money, site_user)
        db_profile.set_profile_minus_money_hold(float(0.2), site_user)
        db_admin.set_status_site('Подтверждено', site_mess)
        await bot.send_message(site_user, f'Сайт {site_mess} подтвержден!\n\nНа ваш баланс зачислено 0.2 Р.')
        await bot.send_message(ADMIN_ID, f'Сайт {site_mess} подтвержден!')
        await state.finish()


@dp.callback_query_handler(text='delete_sites')
async def menu_admin_delete_sites(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(ADMIN_ID, 'Введите ссылку для удаления')
    await AdminSites.delete_st.set()


@dp.message_handler(state=AdminSites.delete_st)
async def admin_delete_sites(message: types.Message, state: FSMContext):
    site_mess = message.text
    if not site_name_exist(name=site_mess):
        await bot.send_message(message.from_user.id, 'Сайта нет в базе')
        await state.finish()
    else:
        site_user = db_find.find_site_user_id(site_mess)
        db_profile.set_profile_minus_money_hold(float(0.2), site_user)
        db_admin.delete_status_site(site_mess)
        await bot.send_message(site_user, f'Сайт {site_mess} удален!\n\nС вашего баланса списано 0.2 Р.')
        await bot.send_message(ADMIN_ID, f'Сайт {site_mess} удален!')
        await state.finish()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(menu_admin, text='admin')
    dp.register_message_handler(menu_admin_phones, text='admin_phones')
    dp.register_message_handler(menu_admin_confirm_phones, text='confirm_phones')
    dp.register_message_handler(admin_confirm_phones, state=AdminPhones.confirm_ph)
    dp.register_message_handler(menu_admin_delete_phones, text='delete_phones')
    dp.register_message_handler(admin_delete_phones, state=AdminPhones.delete_ph)
    dp.register_message_handler(menu_admin_sites, text='admin_sites')
    dp.register_message_handler(menu_admin_confirm_sites, text='confirm_sites')
    dp.register_message_handler(admin_confirm_sites, state=AdminSites.confirm_st)
    dp.register_message_handler(menu_admin_delete_sites, text='delete_sites')
    dp.register_message_handler(admin_delete_sites, state=AdminSites.delete_st)
