import logging
import asyncio
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    BotCommand
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from telegram.constants import ParseMode, ChatAction

from config import TELEGRAM_BOT_TOKEN, ALLOWED_USER_ID
from ai_analyzer import analyze_food_image, is_valid_image


def is_authorized(update: Update) -> bool:
    """Foydalanuvchi ruxsat etilganligini tekshiradi."""
    return update.effective_user is not None and update.effective_user.id == ALLOWED_USER_ID


async def deny_access(update: Update) -> None:
    """Ruxsatsiz foydalanuvchiga javob bermaydi (sukut saqlaydi)."""
    user = update.effective_user
    logger_temp = logging.getLogger(__name__)
    logger_temp.warning(f"Ruxsatsiz kirish urinishi: {user.id} | @{user.username}")
    # Hech qanday javob berilmaydi — bot faqat sukut saqlaydi

# Logging sozlash
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================
# Xabar matni konstantlari (O'zbek tilida)
# ============================================================

WELCOME_MESSAGE = """
🤖 *Kaloriya Hisoblagich Botga Xush Kelibsiz!*

Men sun'iy intellekt yordamida ovqat va mahsulotlaringiz kaloriyasini hisoblayman.

━━━━━━━━━━━━━━━━━━━━━
📸 *Qanday foydalanish mumkin?*

1️⃣ Ovqat yoki mahsulot **rasmini yuboring**
2️⃣ Bot avtomatik ravishda tahlil qiladi
3️⃣ Kaloriya va ozuqa tarkibini ko'rasiz

━━━━━━━━━━━━━━━━━━━━━
🍎 *Nima tahlil qila olaman?*
• Pishirilgan taomlar
• Mevalar va sabzavotlar
• Gazak va shirinliklar
• Ichimliklar
• Paketlangan mahsulotlar

━━━━━━━━━━━━━━━━━━━━━
💡 *Maslahat:* Yaxshi natija uchun rasmni yaqindan va yaxshi yorug'likda oling!

📌 Buyruqlar: /help | /about
"""

HELP_MESSAGE = """
📖 *Yordam va Ko'rsatmalar*

━━━━━━━━━━━━━━━━━━━━━
🔧 *Buyruqlar:*
• /start — Botni ishga tushirish
• /help — Yordam ko'rish
• /about — Bot haqida

━━━━━━━━━━━━━━━━━━━━━
📸 *Foydalanish:*
1. Ovqat rasmini to'g'ridan-to'g'ri chatga yuboring
2. Bir necha soniya kuting (AI tahlil qiladi)
3. Natijani oling

━━━━━━━━━━━━━━━━━━━━━
✅ *Qo'llab-quvvatlanadigan formatlar:*
JPEG, JPG, PNG, WEBP

━━━━━━━━━━━━━━━━━━━━━
❓ *Ko'p so'raladigan savollar:*

❔ Aniqlik qanchalik yuqori?
✅ AI taxminiy hisob beradi, professional o'lchash uchun laboratoriya tahlili kerak.

❔ Bir kunda necha marta foydalana olaman?
✅ Cheksiz, lekin API limiti tugasa vaqtinchalik kutish kerak bo'ladi.
"""

ABOUT_MESSAGE = """
ℹ️ *Bot Haqida*

━━━━━━━━━━━━━━━━━━━━━
🤖 *Kaloriya Hisoblagich Bot*
📌 Versiya: 1.0.0

━━━━━━━━━━━━━━━━━━━━━
🧠 *Texnologiyalar:*
• Python 3.10+
• python-telegram-bot 20+
• Google Gemini 1.5 Flash (AI)

━━━━━━━━━━━━━━━━━━━━━
🌟 *Imkoniyatlar:*
✅ Rasm orqali ovqat tanish
✅ Kaloriya hisoblash
✅ Ozuqa tarkibi tahlili
✅ Dietolog maslahati

━━━━━━━━━━━━━━━━━━━━━
⚡ Powered by Google Gemini AI
"""

ANALYZING_MESSAGE = """
⏳ *Tahlil qilinmoqda...*

🔍 AI rasmingizni ko'rib chiqmoqda
🧪 Kaloriya hisoblanmoqda
📊 Natijalar tayyorlanmoqda

Bir oz kuting...
"""

# ============================================================
# Handler funksiyalari
# ============================================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/ start buyrug'i"""
    if not is_authorized(update):
        await deny_access(update)
        return
    user = update.effective_user
    logger.info(f"Foydalanuvchi botni boshladi: {user.id} | {user.username}")

    keyboard = [
        [
            InlineKeyboardButton("📖 Yordam", callback_data="help"),
            InlineKeyboardButton("ℹ️ Haqida", callback_data="about"),
        ],
        [
            InlineKeyboardButton("🌐 GitHub", url="https://github.com"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        WELCOME_MESSAGE,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/help buyrug'i"""
    if not is_authorized(update):
        await deny_access(update)
        return
    await update.message.reply_text(
        HELP_MESSAGE,
        parse_mode=ParseMode.MARKDOWN
    )


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/about buyrug'i"""
    if not is_authorized(update):
        await deny_access(update)
        return
    await update.message.reply_text(
        ABOUT_MESSAGE,
        parse_mode=ParseMode.MARKDOWN
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Inline tugmalar uchun callback"""
    if not is_authorized(update):
        await deny_access(update)
        return
    query = update.callback_query
    await query.answer()

    if query.data == "help":
        await query.message.reply_text(HELP_MESSAGE, parse_mode=ParseMode.MARKDOWN)
    elif query.data == "about":
        await query.message.reply_text(ABOUT_MESSAGE, parse_mode=ParseMode.MARKDOWN)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Foydalanuvchi yuborgan rasmni qabul qilib AI ga yuboradi
    va kaloriya natijasini qaytaradi.
    """
    if not is_authorized(update):
        await deny_access(update)
        return
    user = update.effective_user
    logger.info(f"Rasm qabul qilindi: {user.id} | {user.username}")

    # "Tahlil qilinmoqda" xabari yuborish
    status_message = await update.message.reply_text(
        ANALYZING_MESSAGE,
        parse_mode=ParseMode.MARKDOWN
    )

    # "Typing..." ko'rsatish
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    try:
        # Eng yuqori sifatli rasmni olish
        photo = update.message.photo[-1]
        photo_file = await context.bot.get_file(photo.file_id)

        # Rasmni yuklab olish
        image_bytes = await photo_file.download_as_bytearray()

        # AI tahlili (async)
        result = await analyze_food_image(bytes(image_bytes))

        # Status xabarini o'chirish
        await status_message.delete()

        # Tugmalar
        keyboard = [
            [
                InlineKeyboardButton("🔄 Yana tahlil qilish", callback_data="analyze_again"),
                InlineKeyboardButton("❓ Yordam", callback_data="help"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Natijani yuborish
        await update.message.reply_text(
            result,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

        logger.info(f"Natija yuborildi: {user.id}")

    except Exception as e:
        logger.error(f"Rasm tahlilida xatolik: {e}")
        await status_message.edit_text(
            "❌ Rasm tahlilida xatolik yuz berdi.\n\n"
            "Iltimos, qayta urinib ko'ring yoki boshqa rasm yuboring.",
            parse_mode=ParseMode.MARKDOWN
        )


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fayl sifatida yuborilgan rasmlarni qayta ishlash"""
    if not is_authorized(update):
        await deny_access(update)
        return
    document = update.message.document

    if document and document.mime_type and is_valid_image(document.mime_type):
        # Fayl rasm bo'lsa, rasm kabi qayta ishlash
        user = update.effective_user
        logger.info(f"Fayl (rasm) qabul qilindi: {user.id} | {user.username}")

        status_message = await update.message.reply_text(
            ANALYZING_MESSAGE,
            parse_mode=ParseMode.MARKDOWN
        )

        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action=ChatAction.TYPING
        )

        try:
            doc_file = await context.bot.get_file(document.file_id)
            image_bytes = await doc_file.download_as_bytearray()

            result = await analyze_food_image(bytes(image_bytes))

            await status_message.delete()

            keyboard = [
                [InlineKeyboardButton("🔄 Yana tahlil qilish", callback_data="analyze_again")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                result,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )

        except Exception as e:
            logger.error(f"Fayl tahlilida xatolik: {e}")
            await status_message.edit_text("❌ Fayl tahlilida xatolik yuz berdi.")
    else:
        await update.message.reply_text(
            "📎 Faqat rasm fayllarini qabul qilaman.\n"
            "✅ Qo'llab-quvvatlanadigan formatlar: JPEG, PNG, WEBP\n\n"
            "📸 Ovqat rasmini yuboring!",
            parse_mode=ParseMode.MARKDOWN
        )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Matn xabarlariga javob berish"""
    if not is_authorized(update):
        await deny_access(update)
        return
    await update.message.reply_text(
        "📸 *Iltimos, ovqat rasmini yuboring!*\n\n"
        "Men faqat rasmlar orqali kaloriya hisoblashim mumkin.\n"
        "Matn qabul qilmayman 😊\n\n"
        "💡 /help — ko'proq ma'lumot",
        parse_mode=ParseMode.MARKDOWN
    )


async def analyze_again_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """'Yana tahlil qilish' tugmasi"""
    if not is_authorized(update):
        await deny_access(update)
        return
    query = update.callback_query
    await query.answer("📸 Yangi rasm yuboring!", show_alert=False)
    await query.message.reply_text(
        "📸 Yangi ovqat rasmini yuboring, tahlil qilaman!",
        parse_mode=ParseMode.MARKDOWN
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Global xato boshqaruvchisi"""
    logger.error(f"Xatolik yuz berdi: {context.error}", exc_info=context.error)


# ============================================================
# Botni ishga tushirish
# ============================================================

async def post_init(application: Application) -> None:
    """Bot ishga tushgandan keyin buyruqlarni o'rnatish"""
    commands = [
        BotCommand("start", "Botni ishga tushirish"),
        BotCommand("help", "Yordam va ko'rsatmalar"),
        BotCommand("about", "Bot haqida ma'lumot"),
    ]
    await application.bot.set_my_commands(commands)
    logger.info("Bot buyruqlari o'rnatildi.")


def main() -> None:
    """Asosiy funksiya — botni ishga tushiradi"""
    import asyncio

    logger.info("=" * 50)
    logger.info("Bot ishga tushmoqda...")
    logger.info("=" * 50)

    # Applicationni yaratish
    application = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    # Handler lar ro'yxatdan o'tkazish
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))

    # Rasm handlerlari
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # Matn handleri
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Callback tugmalar
    application.add_handler(CallbackQueryHandler(analyze_again_callback, pattern="^analyze_again$"))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Xato handleri
    application.add_error_handler(error_handler)

    logger.info("Barcha handlerlar royxatdan otdi.")
    logger.info("Bot polling rejimida ishlamoqda...")

    # Python 3.10+ uchun event loop yaratish
    asyncio.set_event_loop(asyncio.new_event_loop())

    # Botni polling rejimida ishga tushirish
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
