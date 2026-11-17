import os
import logging

from telegram import Update
from telegram.error import TelegramError
from telegram.ext import ContextTypes

from config import ADMIN_IDS, PHOTOS_DIR

logger = logging.getLogger(__name__)

async def feedback_promt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Put foto of the product and feedback"
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    user = update.effective_user
    photo = msg.photo[-1]

    os.makedirs(PHOTOS_DIR, exist_ok=True)
    path = os.path.join(PHOTOS_DIR, f"{user.id}_{photo.file_unique_id}.jpg")
    tg_file = await photo.get_file()
    await tg_file.download_to_drive(path)


    username = f" (@{user.username})" if user.username else ""
    caption = (
        f"Feedback from {user.full_name}{username}\n"
        f"ID: {user.id}\n\n"
        f"{msg.caption or 'no caption'}"
    )

    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_photo(admin_id, photo=photo.file_id, caption=caption[:1024])
        except TelegramError as e:
            logger.warning("Unable to send photo to admin", admin_id, e)
    
    await msg.reply_text(f"thank u for feedback")


async def handle_image_doc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "U send photo as file. Please send it as photo"
    )