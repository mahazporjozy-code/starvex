import os
import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPPORT = "https://t.me/StarvexMahaz"

WELCOME = """
👑 به امپراتوری STARVEX خوش آمدید!

🖤 تجربه‌ای متفاوت از خدمات دیجیتال تلگرام؛
✨ برای کسانی که بهترین‌ها را انتخاب می‌کنند.

💎 پریمیوم | بوست | استارز
⚡ سفارش آسان و پشتیبانی مستقیم

🚀 وارد دنیای STARVEX شوید.
🛡 STARVEX EMPIRE
"""

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👑 تلگرام پریمیوم", callback_data="premium")],
        [InlineKeyboardButton("🚀 تلگرام بوست", callback_data="boost")],
        [InlineKeyboardButton("⭐ تلگرام استارز", callback_data="stars")],
        [InlineKeyboardButton("🛒 ثبت سفارش", callback_data="order")],
        [InlineKeyboardButton("🛟 پشتیبانی", url=SUPPORT)],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if args and args[0] in ("premium", "boost", "stars"):
        product = args[0]

        if product == "premium":
            message = "👑 بخش تلگرام پریمیوم انتخاب شد.\n\nپلن موردنظرت رو انتخاب کن."
        elif product == "boost":
            message = "🚀 بخش تلگرام بوست انتخاب شد.\n\nپلن موردنظرت رو انتخاب کن."
        else:
            message = "⭐ بخش تلگرام استارز انتخاب شد.\n\nبرای سفارش استارز ادامه بده."

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🛍 ادامه سفارش", callback_data=product)],
            [InlineKeyboardButton("🏠 منوی اصلی", callback_data="main_menu")],
            [InlineKeyboardButton("🛟 پشتیبانی", url=SUPPORT)],
        ])

        await update.effective_message.reply_text(
            message,
            reply_markup=keyboard
        )
        return

    await update.effective_message.reply_text(
        WELCOME,
        reply_markup=main_menu()
    )
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "premium":
        text = (
            "👑 تلگرام پریمیوم\n\n"
            "۳ ماهه: ۳٬۵۲۵٬۰۰۰ تومان\n"
            "۶ ماهه: ۴٬۶۰۱٬۰۰۰ تومان\n"
            "یک‌ساله: ۸٬۱۰۰٬۰۰۰ تومان\n\n"
            "برای ثبت سفارش، گزینهٔ ثبت سفارش را بزن."
        )

    elif query.data == "boost":
        text = (
            "🚀 تلگرام بوست\n\n"
            "۱۴ روزه: ۵۹٬۰۰۰ تومان\n"
            "۳۰ روزه: ۱۲۰٬۰۰۰ تومان\n"
            "۹۰ روزه: ۲۲۰٬۰۰۰ تومان\n"
            "۱۸۰ روزه: ۳۹۰٬۰۰۰ تومان\n\n"
            "حداقل سفارش: ۱۰ بوست\n"
            "برای سفارش، گزینهٔ ثبت سفارش را بزن."
        )

    elif query.data == "stars":
        text = (
            "⭐ تلگرام استارز\n\n"
            "قیمت هر استار: ۴٬۵۰۰ تومان\n"
            "حداقل سفارش: ۵۰ استار\n\n"
            "برای سفارش، گزینهٔ ثبت سفارش را بزن."
        )

    elif query.data == "order":
        context.user_data["waiting_order"] = True
        await query.message.reply_text(
            "🛒 برای ثبت درخواست، این اطلاعات را در یک پیام بفرست:\n\n"
            "۱. محصول موردنظر\n"
            "۲. مدت یا تعداد\n\n"
            "مثال: پریمیوم سه‌ماهه\n\n"
            "⚠️ رمز عبور، کد ورود یا کد تأیید تلگرام را نفرست."
        )
        return

    else:
        return

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 ثبت سفارش", callback_data="order")],
        [InlineKeyboardButton("🛟 پشتیبانی", url=SUPPORT)],
        [InlineKeyboardButton("🔙 منوی اصلی", callback_data="home")],
    ])

    if query.data == "home":
        await query.message.reply_text(WELCOME, reply_markup=main_menu())
    else:
        await query.message.reply_text(text, reply_markup=keyboard)

async def receive_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("waiting_order"):
        return

    context.user_data["waiting_order"] = False
    order = update.message.text

    await update.message.reply_text(
        "✅ درخواستت ثبت شد!\n\n"
        "برای هماهنگی و نهایی‌کردن سفارش با پشتیبانی تماس بگیر:\n"
        + SUPPORT
    )

    logging.info("Order request received from user ID %s", update.effective_user.id)

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN در متغیرهای محیطی تنظیم نشده است.")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_order))
    app.run_polling()

if __name__ == "__main__":
    main()