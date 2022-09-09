from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InputFile
from start_bot import dp, bot
from database import db_profile
from keyboards import user_kb


@dp.callback_query_handler(text='profile')
async def menu_profile(call: types.CallbackQuery):
    await call.message.delete()
    text = '➖➖➖➖➖➖'
    p_id = db_profile.profile_id(call.from_user.id)
    p_view = db_profile.profile_view(call.from_user.id)
    p_viewed_phone = db_profile.profile_viewed_phone(call.from_user.id)
    p_viewed_site = db_profile.profile_viewed_site(call.from_user.id)
    await bot.send_message(call.from_user.id, f'{text}\n👤 <b>Профиль: </b>№ {p_id}\n{text}\n'
                                              f'🆔 <b>Айди: </b>{call.from_user.id}\n\n'
                                              f'😎 <b>Юзернейм: </b>@{call.from_user.username}\n\n'
                                              f'👁 <b>Просмотры: </b>{p_view}\n{text}\n'
                                              f'🔎 <b>Запросы:</b>\n{text}\n'
                                              f'📱 <b>Номера: </b>{p_viewed_phone}\n\n'
                                              f'🔗 <b>Сайты: </b>{p_viewed_site}',
                           parse_mode='HTML',
                           reply_markup=user_kb.profile_kb)


@dp.callback_query_handler(text='phone')
async def profile_phone(call: types.CallbackQuery):
    await call.message.delete()
    p_phone = db_profile.profile_phone(call.from_user.id)
    p_phone_count = db_profile.profile_phone_count(call.from_user.id).pop()[0]
    if not p_phone:
        await bot.send_message(call.from_user.id, 'У вас не добавлено ни одного номера',
                               reply_markup=user_kb.profile_exit_kb)
    else:
        await bot.send_message(call.from_user.id, f'📱 <b>Номера ({p_phone_count})</b>\n\n<b>{p_phone}</b>',
                               parse_mode='HTML', reply_markup=user_kb.profile_exit_kb)


@dp.callback_query_handler(text='site')
async def profile_site(call: types.CallbackQuery):
    await call.message.delete()
    p_site = db_profile.profile_site(call.from_user.id)
    p_site_count = db_profile.profile_site_count(call.from_user.id).pop()[0]
    if not p_site:
        await bot.send_message(call.from_user.id, 'У вас не добавлено ни одного сайта',
                               reply_markup=user_kb.profile_exit_kb)
    else:
        await bot.send_message(call.from_user.id, f'🔗 <b>Сайты ({p_site_count})</b>\n\n<b>{p_site}</b>',
                               parse_mode='HTML',
                               reply_markup=user_kb.profile_exit_kb, disable_web_page_preview=True)


def register_handlers_profile(dp: Dispatcher):
    dp.register_message_handler(menu_profile, text='profile')
    dp.register_message_handler(profile_phone, text='phone')
    dp.register_message_handler(profile_site, text='site')
