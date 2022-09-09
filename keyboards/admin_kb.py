from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_kb = InlineKeyboardMarkup(row_width=1)
profile = InlineKeyboardButton('👤 Профиль', callback_data='profile')
add = InlineKeyboardButton('➕ Добавить', callback_data='add')
check = InlineKeyboardButton('‍👁 Проверить', callback_data='check')
admin = InlineKeyboardButton('🤖 Админка', callback_data='admin')
menu_kb.row(check, add).row(profile, admin)

admin_menu_kb = InlineKeyboardMarkup(row_width=1)
phones = InlineKeyboardButton('📱 Номера', callback_data='admin_phones')
sites = InlineKeyboardButton('🔗 Сайты', callback_data='admin_sites')
users = InlineKeyboardButton('👥 Пользователи', callback_data='admin_users')
menu = InlineKeyboardButton('⬅️ Назад', callback_data='menu')
admin_menu_kb.row(phones, sites).row(users).row(menu)

admin_menu_phones_kb = InlineKeyboardMarkup(row_width=1)
confirm_phones = InlineKeyboardButton('✅ Подтвердить', callback_data='confirm_phones')
delete_phones = InlineKeyboardButton('❌ Удалить', callback_data='delete_phones')
admin = InlineKeyboardButton('⬅️ Назад', callback_data='admin')
admin_menu_phones_kb.row(confirm_phones, delete_phones).row(admin)

admin_menu_sites_kb = InlineKeyboardMarkup(row_width=1)
confirm_sites = InlineKeyboardButton('✅ Подтвердить', callback_data='confirm_sites')
delete_sites = InlineKeyboardButton('❌ Удалить', callback_data='delete_sites')
admin = InlineKeyboardButton('⬅️ Назад', callback_data='admin')
admin_menu_sites_kb.row(confirm_sites, delete_sites).row(admin)
