import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# API keys
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Gemini sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""Sen har qanday topshiriqni bajara oladigan aqlli AI yordamchisan.
Foydalanuvchi senga qanday savol bersa yoki topshiriq yuklatsa, uni to'liq va aniq bajarishga harakat qil.
O'zbek tilida so'rashsa o'zbek tilida, rus tilida so'rashsa rus tilida, ingliz tilida so'rashsa ingliz tilida javob ber.
Doim foydali, aniq va tushunarli javoblar ber."""
)

# Har bir foydalanuvchining suhbat tarixini saqlash
user_chats = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_chats[user_id] = model.start_chat(history=[])
    await update.message.reply_text(
        "👋 Salom! Men har qanday topshiriqni bajarishga tayyorman.\n\n"
        "💡 Menga quyidagilarni so'rashingiz mumkin:\n"
        "• Kod yozish\n"
        "• Tarjima qilish\n"
        "• Matn yozish\n"
        "• Savollar javoblash\n"
        "• Va boshqa har qanday narsa!\n\n"
        "Boshlang! 🚀"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 *Buyruqlar:*\n"
        "/start — Botni qayta ishga tushirish\n"
        "/clear — Suhbat tarixini tozalash\n"
        "/help — Yordam\n\n"
        "Menga istalgan savol yoki topshiriq yuboring!",
        parse_mode="Markdown"
    )


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_chats[user_id] = model.start_chat(history=[])
    await update.message.reply_text("🗑️ Suhbat tarixi tozalandi. Yangi suhbat boshlang!")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    # Typing ko'rsatish
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    # Foydalanuvchi chatini olish yoki yangi yaratish
    if user_id not in user_chats:
        user_chats[user_id] = model.start_chat(history=[])

    try:
        chat = user_chats[user_id]
        response = chat.send_message(user_text)
        reply = response.text

        # Telegram 4096 belgidan uzun xabar qabul qilmaydi
        if len(reply) > 4000:
            for i in range(0, len(reply), 4000):
                await update.message.reply_text(reply[i:i+4000])
        else:
            await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(
            "⚠️ Xato yuz berdi. Qaytadan urinib ko'ring.\n"
            f"Xato: {str(e)}"
        )


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot ishga tushdi!")
    app.run_polling()


if __name__ == "__main__":
    main()
