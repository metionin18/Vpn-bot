
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8080797475:AAFoNhwsJ_HsItiI7VRSBRsqT7WxJ_O1YDc"
ADMIN_ID = 8171384352

plans = [
    "🟢 1 ماهه | 100,000 تومان",
    "🔵 3 ماهه | 250,000 تومان",
    "🟣 6 ماهه | 450,000 تومان"
]

card_number = "6037-9911-2345-6789"

user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["🛒 خرید سرویس"], ["📞 دریافت تست رایگان"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("به ربات فروش VPN خوش آمدید! یکی از گزینه‌ها را انتخاب کنید:", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == "🛒 خرید سرویس":
        plan_text = "\n".join([f"{i+1}. {p}" for i, p in enumerate(plans)])
        await update.message.reply_text(f"لطفاً یکی از پلن‌ها را انتخاب کنید:\n\n{plan_text}")
        user_state[user_id] = "selecting_plan"

    elif user_state.get(user_id) == "selecting_plan" and text[0].isdigit():
        await update.message.reply_text(f"شماره کارت برای پرداخت:\n💳 {card_number}\n\nلطفاً پس از پرداخت، رسید خود را ارسال کنید.")
        user_state[user_id] = "awaiting_receipt"

    elif user_state.get(user_id) == "awaiting_receipt":
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"🧾 رسید پرداخت از کاربر @{update.effective_user.username or 'بدون نام'}:

{text}")
        await update.message.reply_text("رسید شما ارسال شد. پس از تأیید، سرویس برای شما فعال می‌شود.")
        user_state.pop(user_id, None)

    elif text == "📞 دریافت تست رایگان":
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"📞 درخواست تست رایگان از کاربر: @{update.effective_user.username or 'بدون نام'}")
        await update.message.reply_text("درخواست شما برای ادمین ارسال شد. در صورت تأیید، با شما تماس گرفته می‌شود.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_state.get(user_id) == "awaiting_receipt":
        photo = update.message.photo[-1]
        file_id = photo.file_id
        await context.bot.send_photo(chat_id=ADMIN_ID, photo=file_id, caption=f"🧾 رسید عکس از کاربر @{update.effective_user.username or 'بدون نام'}")
        await update.message.reply_text("رسید شما ارسال شد. پس از تأیید، سرویس برای شما فعال می‌شود.")
        user_state.pop(user_id, None)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

if __name__ == "__main__":
    print("ربات روشن شد...")
    app.run_polling()
