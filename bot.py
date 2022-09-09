from aiogram.utils import executor
from start_bot import dp
from handlers import main, add, find, profile, wallet, admin

admin.register_handlers_admin(dp)
main.register_handlers_main(dp)
add.register_handlers_add(dp)
find.register_handlers_find(dp)
profile.register_handlers_profile(dp)
wallet.register_handlers_wallet(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)