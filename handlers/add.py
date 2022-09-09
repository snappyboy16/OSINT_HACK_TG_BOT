from aiogram.types import InputFile
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import sqlite3
from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from start_bot import dp, bot
from database import db_add, db_profile, db_find
from keyboards import user_kb
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


class UserSite(StatesGroup):
    site = State()
    site_type = State()


class UserPhone(StatesGroup):
    phone = State()
    phone_type = State()


@dp.callback_query_handler(text='add')
async def menu_add(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, 'Выберите что добавить', reply_markup=user_kb.add_kb)


@dp.callback_query_handler(text='add_phone')
async def menu_add_phone(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, 'Введите номер телефона')
    await UserPhone.phone.set()


@dp.message_handler(state=UserPhone.phone)
async def user_add_phone(message: types.Message, state: FSMContext):
    global phone_num, info_phone_clear
    phone_num = message.text
    if not phone_num_exist(phone=phone_num):
        if len(phone_num) == 11:
            if phone_num.isdigit():
                browser = webdriver.Chrome('driver/chromedriver.exe')
                browser.get('https://phonenum.info/phone/')
                sleep(1)
                await bot.send_message(message.from_user.id, '🔎 Собираю информацию о номере...')
                browser.find_element(By.XPATH, '//*[@id="phoneInput"]').send_keys(phone_num)
                browser.find_element(By.XPATH, '//*[@id="mainContainer"]/form/input[2]').click()
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1,
                                            text='🏙 Получаю регион...')
                sleep(1)
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1,
                                            text='📡 Получаю оператора...')
                sleep(1)
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1,
                                            text='🛡 Сохраняю информацию...')
                info_phone = browser.find_elements(By.CLASS_NAME, 'paramValue')
                info_phone_clear = [div.text.replace('"', ' ') for div in info_phone]
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1,
                                            text='🎉 Готово')
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1,
                                            text='Выберите тип', reply_markup=user_kb.add_phone_types)
                await UserPhone.phone_type.set()
            else:
                await bot.send_message(message.from_user.id, 'Введите номер а не текст, попробуйте ещё раз',
                                       reply_markup=user_kb.start_menu_kb)
                await state.finish()
        else:
            await bot.send_message(message.from_user.id, 'Номер введён не правильно, попробуйте ещё раз',
                                   reply_markup=user_kb.start_menu_kb)
            await state.finish()
    else:
        await bot.send_message(message.from_user.id, 'Этот номер уже добавлен!', reply_markup=user_kb.start_menu_kb)
        await state.finish()


@dp.callback_query_handler(text='spam', state=UserPhone.phone_type)
async def type_spam_add_phone(call: types.CallbackQuery, state: FSMContext):
    db_add.add_phone(call.from_user.id, call.from_user.username, phone_num, info_phone_clear[3:4].pop()[0:-1],
                     info_phone_clear[2:3].pop()[0:-1], 'Спам', 0, 'Ожидание')
    db_profile.set_profile_money_hold(0.2, call.from_user.id)
    phone_reg = db_find.find_phone_reg(phone_num)
    phone_oper = db_find.find_phone_oper(phone_num)
    phone_type = db_find.find_phone_type(phone_num)
    phone_view = db_find.find_phone_view(phone_num)
    phone_user = db_find.find_phone_user(phone_num)
    await call.message.delete()
    await bot.send_message(call.from_user.id, 'Спасибо за вашу бдительность - тип: Спам')
    await bot.send_message(ADMIN_ID, f'📱 <b>Номер:</b> +{phone_num}\n\n'
                                     f'🏙 <b>Регион:</b> {phone_reg}\n\n'
                                     f'🏢 <b>Оператор:</b> {phone_oper}\n\n'
                                     f'⚠️<b> Вид номера:</b> {phone_type}\n\n'
                                     f'👁 <b> Просмотров: </b>{phone_view}\n\n'
                                     f'👤 <b> Добавлен:</b> @{phone_user}\n\n'
                           , parse_mode='HTML')
    await state.finish()


@dp.callback_query_handler(text='ad', state=UserPhone.phone_type)
async def type_ad_add_phone(call: types.CallbackQuery, state: FSMContext):
    db_add.add_phone(call.from_user.id, call.from_user.username, phone_num, info_phone_clear[3:4].pop()[0:-1],
                     info_phone_clear[2:3].pop()[0:-1], 'Реклама', 0, 'Ожидание')
    db_profile.set_profile_money_hold(0.2, call.from_user.id)
    await call.message.delete()
    await bot.send_message(call.from_user.id, 'Спасибо за вашу бдительность - тип: Реклама')
    await state.finish()


@dp.callback_query_handler(text='add_site')
async def menu_add_site(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, 'Введите ссылку на сайт')
    await UserSite.site.set()


@dp.message_handler(state=UserSite.site)
async def user_add_site(message: types.Message, state: FSMContext):
    global site_link, site_name_clear, site_ip_clear, site_registrator_clear, site_server_one_clear
    global site_fin_clear, site_reg_clear, site_web_archive
    site_link = message.text
    sep_site = 'https://' or 'http://'
    site_link_clear = site_link.replace(sep_site, '')
    ua = UserAgent()
    user_agent = ua.random
    options = Options()
    options.add_argument(f'user-agent={user_agent}')
    suite = webdriver.Chrome('driver/chromedriver.exe', chrome_options=options)
    if not 'https://' in message.text or 'http://' in message.text:
        await bot.send_message(message.from_user.id, 'Введите правильную ссылку')
        await state.finish()
    else:
        if not '/' in site_link_clear:
            if not site_name_exist(name=site_link_clear):
                await bot.send_message(message.from_user.id, '🔑 Открываю сайт...')
                suite.get('https://be1.ru/stat/')
                suite.find_element(By.XPATH, '//*[@id="tool-form"]/div/input').send_keys(site_link)
                suite.find_element(By.XPATH, '//*[@id="tool-form"]/div/span').click()
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1,
                                            text='🔎 Собираю информацию о сайте...')
                sleep(5)
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1,
                                            text='📃 Получаю имя...')
                site_name = suite.find_elements(By.XPATH, '//*[@id="set_whois"]/div/div[1]/table/tbody/tr[1]/td[2]')
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1,
                                            text='🌐 Получаю регистратора...')
                sleep(1)
                site_registrator = suite.find_elements(By.XPATH,
                                                       '//*[@id="set_whois"]/div/div[2]/table/tbody/tr[1]/td[2]')
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1,
                                            text='📅 Получаю информацию о домене...')
                sleep(1)
                site_reg = suite.find_elements(By.XPATH, '//*[@id="set_whois"]/div/div[1]/table/tbody/tr[2]/td[2]')
                site_fin = suite.find_elements(By.XPATH, '//*[@id="set_whois"]/div/div[1]/table/tbody/tr[3]/td[2]')
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1,
                                            text='🛡 Сохраняю информацию...')
                site_name_clear = [div.text.replace('"', ' ') for div in site_name]
                site_registrator_clear = [div.text.replace('"', ' ') for div in site_registrator]
                site_reg_clear = [div.text.replace('"', ' ') for div in site_reg]
                site_fin_clear = [div.text.replace('"', ' ') for div in site_fin]
                site_web_archive = 'https://web.archive.org/web/*/' + site_link
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1,
                                            text='🎉 Готово')
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1,
                                            text='Выберите тип сайта', reply_markup=user_kb.add_site_types)
                await state.finish()
            else:
                await bot.send_message(message.from_user.id, 'Сайт уже есть в базе!')
                await state.finish()
        else:
            site_link_db = site_link_clear[0:site_link_clear.index('/')]
            if not site_name_exist(name=site_link_db):
                await bot.send_message(message.from_user.id, '🔑 Открываю сайт...')
                suite.get('https://be1.ru/stat/')
                suite.find_element(By.XPATH, '//*[@id="tool-form"]/div/input').send_keys(site_link)
                suite.find_element(By.XPATH, '//*[@id="tool-form"]/div/span').click()
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1,
                                            text='🔎 Собираю информацию о сайте...')
                sleep(5)
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1,
                                            text='📃 Получаю имя...')
                site_name = suite.find_elements(By.XPATH, '//*[@id="set_whois"]/div/div[1]/table/tbody/tr[1]/td[2]')
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1,
                                            text='🌐 Получаю регистратора...')
                sleep(1)
                site_registrator = suite.find_elements(By.XPATH,
                                                       '//*[@id="set_whois"]/div/div[2]/table/tbody/tr[1]/td[2]')
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1,
                                            text='📅 Получаю информацию о домене...')
                sleep(1)
                site_reg = suite.find_elements(By.XPATH, '//*[@id="set_whois"]/div/div[1]/table/tbody/tr[2]/td[2]')
                site_fin = suite.find_elements(By.XPATH, '//*[@id="set_whois"]/div/div[1]/table/tbody/tr[3]/td[2]')
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1,
                                            text='🛡 Сохраняю информацию...')
                site_name_clear = [div.text.replace('"', ' ') for div in site_name]
                site_registrator_clear = [div.text.replace('"', ' ') for div in site_registrator]
                site_reg_clear = [div.text.replace('"', ' ') for div in site_reg]
                site_fin_clear = [div.text.replace('"', ' ') for div in site_fin]
                site_web_archive = 'https://web.archive.org/web/*/' + site_link
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1,
                                            text='🎉 Готово')
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1,
                                            text='Выберите тип сайта', reply_markup=user_kb.add_site_types)
                await state.finish()
            else:
                await bot.send_message(message.from_user.id, 'Сайт уже есть в базе!')
                await state.finish()


@dp.callback_query_handler(text='scam')
async def type_scam_add_site(call: types.CallbackQuery):
    db_add.add_site(call.from_user.id, call.from_user.username, site_link, site_name_clear.pop(),
                    site_registrator_clear.pop(), site_reg_clear.pop(), site_fin_clear.pop(), site_web_archive, 'Скам',
                    0, 'Ожидание')
    db_profile.set_profile_money_hold(0.2, call.from_user.id)
    await call.message.delete()
    await bot.send_message(call.from_user.id, 'Спасибо за бдительность сайт - тип: Скам')


def register_handlers_add(dp: Dispatcher):
    dp.register_message_handler(menu_add, text='add')
    dp.register_message_handler(menu_add_phone, text='add_phone')
    dp.register_message_handler(user_add_phone, state=UserPhone.phone)
    dp.register_message_handler(type_spam_add_phone, text='spam', state=UserPhone.phone_type)
    dp.register_message_handler(type_ad_add_phone, text='ad', state=UserPhone.phone_type)
    dp.register_message_handler(menu_add_site, text='add_site')
    dp.register_message_handler(user_add_site, state=UserSite.site)
