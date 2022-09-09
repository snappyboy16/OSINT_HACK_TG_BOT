from aiogram import types, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InputFile
from start_bot import dp, bot
from database import db_profile, db_wallet
from keyboards import user_kb


class WallerSettings(StatesGroup):
    sber = State()
    tinkoff = State()


@dp.callback_query_handler(text='wallet')
async def profile_wallet(call: types.CallbackQuery):
    text = '➖➖➖➖➖➖'
    w_id = db_profile.profile_id(call.from_user.id)
    w_money = db_profile.profile_money(call.from_user.id)
    w_money_hold = db_profile.profile_money_hold(call.from_user.id)
    w_money_withdraw = db_profile.profile_money_withdraw(call.from_user.id)
    w_money_sber = db_profile.profile_money_sber(call.from_user.id)
    w_money_tinkoff = db_profile.profile_money_tinkoff(call.from_user.id)
    await call.message.delete()
    await bot.send_message(call.from_user.id, f'{text}\n💎 <b>Кошелёк: </b>№ {w_id}\n{text}\n'
                                              f'💰 <b>Заработано: </b>{w_money} <b>₽</b>\n\n'
                                              f'🔰 <b>Холд: </b>{w_money_hold} <b>₽</b>\n\n'
                                              f'💸 <b>Выведено: </b>{w_money_withdraw} <b>₽</b>\n{text}\n'
                                              f'🟢 <b>Сбер: </b>{w_money_sber}\n\n'
                                              f'⚫️ <b>Тинькофф: </b>{w_money_tinkoff}',
                           parse_mode='HTML', reply_markup=user_kb.wallet_kb)


@dp.callback_query_handler(text='settings_wallet')
async def wallet_settings(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, f'Выберите действие',
                           reply_markup=user_kb.wallet_settings_kb)


@dp.callback_query_handler(text='settings_sber')
async def wallet_settings_sber(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, 'Введите Сбер номер телефона')
    await WallerSettings.sber.set()


@dp.message_handler(state=WallerSettings.sber)
async def settings_sber(message: types.Message, state: FSMContext):
    sber_mess = message.text
    if '+' in sber_mess:
        sber_mess_clear = sber_mess[1:]
        await bot.send_message(message.from_user.id, f'Сбер номер {sber_mess_clear} успешно сохранился')
        db_wallet.set_wallet_sber(sber_mess_clear, message.from_user.id)
        await state.finish()
    elif not '+' in sber_mess:
        if len(sber_mess) == 11:
            await bot.send_message(message.from_user.id, f'Сбер номер {sber_mess} успешно сохранился')
            db_wallet.set_wallet_sber(sber_mess, message.from_user.id)
            await state.finish()
        else:
            await bot.send_message(message.from_user.id, 'Неправильно набран номер')
            await state.finish()
    else:
        await bot.send_message(message.from_user.id, 'Я тебя не понимаю')
        await state.finish()


@dp.callback_query_handler(text='settings_tinkoff')
async def wallet_settings_tinkoff(call: types.CallbackQuery):
    await call.message.delete()
    await bot.send_message(call.from_user.id, 'Введите Сбер номер телефона')
    await WallerSettings.sber.set()


@dp.message_handler(state=WallerSettings.sber)
async def settings_tinkoff(message: types.Message, state: FSMContext):
    tinkoff_mess = message.text
    if '+' in tinkoff_mess:
        tinkoff_mess_clear = tinkoff_mess[1:]
        await bot.send_message(message.from_user.id, f'Сбер номер {tinkoff_mess_clear} успешно сохранился')
        db_wallet.set_wallet_tinkoff(tinkoff_mess_clear, message.from_user.id)
        await state.finish()
    elif not '+' in tinkoff_mess:
        if len(tinkoff_mess) == 11:
            await bot.send_message(message.from_user.id, f'Сбер номер {tinkoff_mess} успешно сохранился')
            db_wallet.set_wallet_tinkoff(tinkoff_mess, message.from_user.id)
            await state.finish()
        else:
            await bot.send_message(message.from_user.id, 'Неправильно набран номер')
            await state.finish()
    else:
        await bot.send_message(message.from_user.id, 'Я тебя не понимаю')
        await state.finish()


def register_handlers_wallet(dp : Dispatcher):
    dp.register_message_handler(profile_wallet, text='wallet')
    dp.register_message_handler(wallet_settings, text='settings_walllet')
    dp.register_message_handler(wallet_settings_sber, text='settings_sber')
    dp.register_message_handler(settings_sber, state=WallerSettings.sber)
    dp.register_message_handler(wallet_settings_tinkoff, text='settings_tinkoff')
    dp.register_message_handler(settings_tinkoff, state=WallerSettings.tinkoff)