from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Hello, {user.first_name} \n"
        f"Welcome to the ShopBot" 
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Commands: \n"
        f"/start to start the bot \n"
        f"/help to get all commands \n" 
        f"/myID to check personal Telegram ID \n" 
        f"/start to start the bot \n" 
    )

async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Your Telegram ID: {update.effective_user.id}")

    # /start hello world
    # context.args # -> ["hello" "world"] 