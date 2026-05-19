import os

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from database import (
    add_premium,
    is_premium,
    save_memory,
    get_memory,
)

from ai import ask_ai
from vision import analyze_image
from memory import can_use_free

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

admins = os.getenv("ADMIN_IDS", "")

ADMIN_IDS = [
    int(x)
    for x in admins.split(",")
    if x.strip()
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "🔥 AUREVON Aktif\n\n"
        "Özellikler:\n"
        "• AI sohbet\n"
        "• Hafızalı sistem\n"
        "• Görsel analiz\n"
        "• Sesli mesaj AI\n"
        "• Premium üyelik\n"
        "• VIP özellikler"
    )

    await update.message.reply_text(text)


async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "💎 PREMIUM\n\n"
        "• sınırsız mesaj\n"
        "• güçlü AI modeli\n"
        "• hızlı cevap\n"
        "• AI vision\n"
        "• VIP komutlar\n"
        "• özel grup erişimi"
    )

    await update.message.reply_text(text)


async def addpremium_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id not in ADMIN_IDS:
        return

    try:
        target_id = int(context.args[0])

        add_premium(target_id)

        await update.message.reply_text(
            f"✅ {target_id} premium yapıldı."
        )

    except:
        await update.message.reply_text(
            "Kullanım: /addpremium USER_ID"
        )


async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    premium_user = is_premium(user_id)

    if not premium_user:

        if not can_use_free(user_id):

            await update.message.reply_text(
                "❌ Günlük limit doldu.\n/premium"
            )

            return

    text = update.message.text

    await update.message.chat.send_action("typing")

    try:

        memories = get_memory(user_id)

        response = ask_ai(
            text,
            memories,
            premium=premium_user
        )

        save_memory(user_id, "user", text)
        save_memory(user_id, "assistant", response)

        if len(response) > 4000:
            response = response[:4000]

        await update.message.reply_text(response)

    except Exception as e:

        await update.message.reply_text(
            f"❌ Hata:\n{e}"
        )


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await analyze_image(update)


async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🎤 Sesli mesaj AI sistemi yakında aktif olacak."
    )


async def document_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📄 Dosya analiz sistemi aktif değil."
    )


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("premium", premium))
app.add_handler(CommandHandler("addpremium", addpremium_cmd))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        ai_chat
    )
)

app.add_handler(
    MessageHandler(
        filters.PHOTO,
        photo_handler
    )
)

app.add_handler(
    MessageHandler(
        filters.VOICE,
        voice_handler
    )
)

app.add_handler(
    MessageHandler(
        filters.Document.ALL,
        document_handler
    )
)

print("AUREVON AI çalışıyor...")

app.run_polling()
