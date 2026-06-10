import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import tempfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = "8904349425:AAFX-w6dixSyCKu0u2TfaqJWXUzus95sNvw"
GEMINI_API_KEY = "AQ.Ab8RN6KrlEcekxpxGzKo2h2fddNy_0N2BtHY9KhF08J0mcouAw"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")
vision_model = genai.GenerativeModel("gemini-2.0-flash")
chat_sessions = {}

SYSTEM_PROMPT = """Sen universal AI assistantsan. Har qanday vazifani bajara olasan. Uzbek tilida javob ber."""async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_sessions[user_id] = model.start_chat(history=[])
    await update.message.reply_text(
        "👋 Salom! Men universal AI botman!\n\n"
        "💬 Suhbat\n🌐 Tarjima\n💻 Kod yozish\n"
        "🖼️ Rasm tahlil\n🎥 Video tahlil\n📝 Matn yozish\n\n"
        "Xabar yozing yoki fayl yuboring! 🚀"
    )

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_sessions[user_id] = model.start_chat(history=[])
    await update.message.reply_text("✅ Suhbat tarixi tozalandi!")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    if user_id not in chat_sessions:
        chat_sessions[user_id] = model.start_chat(history=[])
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        full_message = f"{SYSTEM_PROMPT}\n\nFoydalanuvchi: {user_message}"
        response = chat_sessions[user_id].send_message(full_message)
        reply = response.text
        if len(reply) > 4096:
            for i in range(0, len(reply), 4096):
                await update.message.reply_text(reply[i:i+4096])
        else:
            await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Xato: {str(e)}")async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
            await file.download_to_drive(tmp.name)
            import PIL.Image
            img = PIL.Image.open(tmp.name)
            caption = update.message.caption or "Bu rasmni batafsil tahlil qil"
            response = vision_model.generate_content([caption, img])
            await update.message.reply_text(f"🖼️ Rasm tahlili:\n\n{response.text}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Xato: {str(e)}")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        video = update.message.video or update.message.document
        file = await context.bot.get_file(video.file_id)
        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp:
            await file.download_to_drive(tmp.name)
            caption = update.message.caption or "Bu videoni tahlil qil"
            video_file = genai.upload_file(tmp.name)
            response = vision_model.generate_content([caption, video_file])
            await update.message.reply_text(f"🎥 Video tahlili:\n\n{response.text}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Xato: {str(e)}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    logger.info("Bot ishga tushdi!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
