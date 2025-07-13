from aiogram import types, Dispatcher

async def cmd_start(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🛒 خرید سرویس", "📞 پشتیبانی")
    await message.answer("سلام! به ربات فروش VPN خوش اومدی 👋", reply_markup=kb)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'])
