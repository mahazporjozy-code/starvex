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
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
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

    # Handle navigation callbacks before product callbacks.
    if query.data in ("home", "main_menu"):
        await query.message.reply_text(WELCOME, reply_markup=main_menu())
        return

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

    await query.message.reply_text(text, reply_markup=keyboard)

async def receive_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("waiting_order"):
        return

    order = (update.message.text or "").strip()
    if not order:
        await update.message.reply_text("لطفاً جزئیات سفارش را به‌صورت متن ارسال کن.")
        return

    if not ADMIN_CHAT_ID:
        context.user_data["waiting_order"] = False
        logging.error("Order intake unavailable: ADMIN_CHAT_ID is not configured.")
        await update.message.reply_text(
            "⚠️ ثبت خودکار سفارش در حال حاضر فعال نیست.\n"
            "برای ثبت و پیگیری درخواست، مستقیماً با پشتیبانی تماس بگیر:\n"
            + SUPPORT
        )
        return

    customer = update.effective_user
    username = f"@{customer.username}" if customer.username else "ندارد"
    admin_message = (
        "🛒 درخواست سفارش جدید STARVEX\\n\\n"
        f"شناسه کاربر: {customer.id}\\n"
        f"نام کاربری: {username}\\n"
        f"نام: {customer.full_name}\\n\\n"
        f"جزئیات درخواست:\\n{order}"
    )

    try:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)
    except Exception:
        logging.exception("Failed to deliver order from user ID %s", customer.id)
        await update.message.reply_text(
            "⚠️ ارسال درخواست به مدیریت انجام نشد. لطفاً دوباره تلاش کن "
            "یا با پشتیبانی تماس بگیر:\\n" + SUPPORT
        )
        return

    context.user_data["waiting_order"] = False
    await update.message.reply_text(
        "✅ درخواستت با موفقیت برای مدیریت ارسال شد. "
        "برای پیگیری بیشتر می‌توانی با پشتیبانی در ارتباط باشی:\\n" + SUPPORT
    )
    logging.info("Order request delivered for user ID %s", customer.id)

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