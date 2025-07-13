from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from handlers import start, buy, admin

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

start.register_handlers(dp)
buy.register_handlers(dp)
admin.register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
