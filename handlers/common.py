from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.messaged.reply_text(
        f"Hello, {user.first_name} \n"
        f"Welcome to the ShopBot" 
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.messaged.reply_text(
        f"COmmands: \n"
        f"/start to start the bot"
        f"/help to get all commands" 
        f"/start to start the bot" 
        f"/start to start the bot" 
    )

