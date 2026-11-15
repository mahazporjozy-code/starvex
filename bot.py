import logging
import os

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.error import TelegramError
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
SUPPORT = "https://t.me/StarvexMahaz"
ADMIN_CHAT_ID_RAW = os.getenv("ADMIN_CHAT_ID")
ADMIN_CHAT_ID = int(ADMIN_CHAT_ID_RAW) if ADMIN_CHAT_ID_RAW else None
MAX_ORDER_LENGTH = 2000

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
    context.user_data.pop("waiting_order", None)
    args = context.args

    if args and args[0] in ("premium", "boost", "stars"):
        product = args[0]
        labels = {
            "premium": "👑 بخش تلگرام پریمیوم انتخاب شد.\n\nپلن موردنظرت رو انتخاب کن.",
            "boost": "🚀 بخش تلگرام بوست انتخاب شد.\n\nپلن موردنظرت رو انتخاب کن.",
            "stars": "⭐ بخش تلگرام استارز انتخاب شد.\n\nبرای سفارش استارز ادامه بده.",
        }
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🛍 ادامه سفارش", callback_data="order")],
            [InlineKeyboardButton("🏠 منوی اصلی", callback_data="main_menu")],
            [InlineKeyboardButton("🛟 پشتیبانی", url=SUPPORT)],
        ])
        await update.effective_message.reply_text(
            labels[product],
            reply_markup=keyboard,
        )
        return

    await update.effective_message.reply_text(WELCOME, reply_markup=main_menu())


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Both callback names are supported so old inline keyboards keep working.
    if query.data in ("main_menu", "home"):
        context.user_data.pop("waiting_order", None)
        await query.message.reply_text(WELCOME, reply_markup=main_menu())
        return

    if query.data == "order":
        context.user_data["waiting_order"] = True
        await query.message.reply_text(
            "🛒 برای ارسال درخواست، محصول و مدت یا تعداد موردنظر را در یک پیام بنویس.\n\n"
            "مثال: پریمیوم سه‌ماهه\n\n"
            "⚠️ رمز عبور، کد ورود یا کد تأیید تلگرام را ارسال نکن.\n"
            "برای لغو، دستور /cancel را بفرست."
        )
        return

    product_messages = {
        "premium": (
            "👑 تلگرام پریمیوم\n\n"
            "۳ ماهه: ۳٬۵۲۵٬۰۰۰ تومان\n"
            "۶ ماهه: ۴٬۶۰۱٬۰۰۰ تومان\n"
            "یک‌ساله: ۸٬۱۰۰٬۰۰۰ تومان\n\n"
            "برای ثبت درخواست، گزینهٔ ثبت سفارش را بزن."
        ),
        "boost": (
            "🚀 تلگرام بوست\n\n"
            "۱۴ روزه: ۵۹٬۰۰۰ تومان\n"
            "۳۰ روزه: ۱۲۰٬۰۰۰ تومان\n"
            "۹۰ روزه: ۲۲۰٬۰۰۰ تومان\n"
            "۱۸۰ روزه: ۳۹۰٬۰۰۰ تومان\n\n"
            "حداقل سفارش: ۱۰ بوست\n"
            "برای ثبت درخواست، گزینهٔ ثبت سفارش را بزن."
        ),
        "stars": (
            "⭐ تلگرام استارز\n\n"
            "قیمت هر استار: ۴٬۵۰۰ تومان\n"
            "حداقل سفارش: ۵۰ استار\n\n"
            "برای ثبت درخواست، گزینهٔ ثبت سفارش را بزن."
        ),
    }

    message = product_messages.get(query.data)
    if message is None:
        await query.message.reply_text(
            "این گزینه شناخته نشد. از منوی اصلی دوباره انتخاب کن.",
            reply_markup=main_menu(),
        )
        return

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 ثبت سفارش", callback_data="order")],
        [InlineKeyboardButton("🛟 پشتیبانی", url=SUPPORT)],
        [InlineKeyboardButton("🔙 منوی اصلی", callback_data="main_menu")],
    ])
    await query.message.reply_text(message, reply_markup=keyboard)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop("waiting_order", None)
    await update.effective_message.reply_text(
        "درخواست ثبت سفارش لغو شد.",
        reply_markup=main_menu(),
    )


async def receive_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("waiting_order"):
        return

    order_text = (update.effective_message.text or "").strip()
    if not order_text:
        await update.effective_message.reply_text("متن درخواست خالی است. لطفاً دوباره ارسال کن.")
        return

    if len(order_text) > MAX_ORDER_LENGTH:
        await update.effective_message.reply_text(
            "متن درخواست خیلی طولانی است. لطفاً آن را کوتاه‌تر و حداکثر در ۲۰۰۰ نویسه ارسال کن."
        )
        return

    if ADMIN_CHAT_ID is None:
        context.user_data.pop("waiting_order", None)
        logger.error("Order was not submitted because ADMIN_CHAT_ID is not configured.")
        await update.effective_message.reply_text(
            "⚠️ دریافت خودکار سفارش هنوز فعال نشده است.\n"
            "برای ثبت درخواست، مستقیماً با پشتیبانی STARVEX تماس بگیر:\n"
            + SUPPORT
        )
        return

    user = update.effective_user
    username = f"@{user.username}" if user.username else "ندارد"
    admin_message = (
        "🛒 درخواست سفارش جدید STARVEX\n\n"
        f"شناسه کاربر: {user.id}\n"
        f"نام کاربری: {username}\n"
        f"نام نمایشی: {user.full_name}\n\n"
        "جزئیات درخواست:\n"
        f"{order_text}"
    )

    try:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)
    except TelegramError:
        logger.exception("Could not deliver an order notification to the configured admin.")
        context.user_data.pop("waiting_order", None)
        await update.effective_message.reply_text(
            "⚠️ ارسال درخواست به مدیریت با مشکل روبه‌رو شد.\n"
            "لطفاً از طریق پشتیبانی پیگیری کن:\n"
            + SUPPORT
        )
        return

    context.user_data.pop("waiting_order", None)
    await update.effective_message.reply_text(
        "✅ درخواستت با موفقیت برای مدیریت STARVEX ارسال شد.\n"
        "برای پیگیری هم می‌توانی از پشتیبانی کمک بگیری:\n"
        + SUPPORT,
        reply_markup=main_menu(),
    )
    logger.info("Order notification delivered for Telegram user ID %s", user.id)


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN در متغیرهای محیطی تنظیم نشده است.")

    if ADMIN_CHAT_ID_RAW:
        try:
            int(ADMIN_CHAT_ID_RAW)
        except ValueError as exc:
            raise RuntimeError("ADMIN_CHAT_ID باید یک شناسه عددی تلگرام باشد.") from exc

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cancel", cancel))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_order))
    app.run_polling()


if __name__ == "__main__":
    main()
