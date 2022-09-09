from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_menu_kb = InlineKeyboardMarkup(row_width=1)
menu = InlineKeyboardButton('🏠 Меню', callback_data='menu')
start_menu_kb.row(menu)

check_channel_kb = InlineKeyboardMarkup(row_width=1)
channel = InlineKeyboardButton('📣 Канал', url='https://t.me/hackscamcommunity', )
sub = InlineKeyboardButton('🔑 Получить доступ', callback_data='check_channel')
check_channel_kb.row(channel).row(sub)

menu_kb = InlineKeyboardMarkup(row_width=1)
profile = InlineKeyboardButton('👤 Профиль', callback_data='profile')
add = InlineKeyboardButton('➕ Добавить', callback_data='add')
check = InlineKeyboardButton('‍👁 Проверить', callback_data='check')
menu_kb.row(check, add).row(profile)


add_kb = InlineKeyboardMarkup(row_width=1)
phone = InlineKeyboardButton('📱 Номер', callback_data='add_phone')
suite = InlineKeyboardButton('🔗 Сайт', callback_data='add_site')
add_kb.row(phone, suite)

profile_kb = InlineKeyboardMarkup(row_width=1)
phone = InlineKeyboardButton('📱 Мои Номера', callback_data='phone')
site = InlineKeyboardButton('🔗 Мои Сайты', callback_data='site')
faq = InlineKeyboardButton('⁉️FAQ', callback_data='faq')
wallet = InlineKeyboardButton('💎 Кошелёк', callback_data='wallet')
menu = InlineKeyboardButton('⬅️ Назад', callback_data='menu')
profile_kb.row(phone, site).row(wallet, faq).row(menu)

wallet_kb = InlineKeyboardMarkup(row_width=1)
withdraw = InlineKeyboardButton('💸 Вывод', callback_data='withdraw')
settings_wallet = InlineKeyboardButton('⚙ Настройки', callback_data='settings_wallet')
history_wallet = InlineKeyboardButton('🗃 История', callback_data='history_wallet')
menu = InlineKeyboardButton('⬅️ Назад', callback_data='profile')
wallet_kb.row(withdraw).row(settings_wallet, history_wallet).row(menu)

wallet_settings_kb = InlineKeyboardMarkup(row_width=1)
sber_settings = InlineKeyboardButton('🟢 Изменить Сбер', callback_data='settings_sber')
tinkoff_settings = InlineKeyboardButton('⚫️ Изменить Тинькофф', callback_data='settings_tinkoff')
wallet = InlineKeyboardButton('⬅️ Назад', callback_data='wallet')
wallet_settings_kb.row(sber_settings, tinkoff_settings).row(wallet)

profile_exit_kb = InlineKeyboardMarkup(row_width=1)
profile = InlineKeyboardButton('⬅️ Назад', callback_data='profile')
faq = InlineKeyboardButton('⁉️FAQ', callback_data='faq')
menu = InlineKeyboardButton('🏠 Меню', callback_data='menu')
profile_exit_kb.row(profile).row(faq).row(menu)

add_phone_types = InlineKeyboardMarkup(row_width=1)
spam = InlineKeyboardButton('Спам', callback_data='spam')
ad = InlineKeyboardButton('Реклама', callback_data='ad')
add_phone_types.row(spam, ad)

add_site_types = InlineKeyboardMarkup(row_width=1)
scam = InlineKeyboardButton('Скам', callback_data='scam')
phishing = InlineKeyboardButton('Фишинг', callback_data='phishing')
add_site_types.row(scam, phishing)