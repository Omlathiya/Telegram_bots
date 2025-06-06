import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me an Instagram Reel link and I will forward it to the channel.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    user_id = update.message.from_user.id
    try:
        filename = f"reel_{user_id}.mp4"
        ydl_opts = {
            'outtmpl': filename,
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'cookiefile': 'cookies.txt',
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open(filename, 'rb') as video:
            await context.bot.send_video(chat_id=update.effective_chat.id, video=video)
            video.seek(0)
            await context.bot.send_video(chat_id=CHANNEL_ID, video=video)

        os.remove(filename)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
