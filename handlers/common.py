from telegram import Update
from telegram.ext import ContextTypes
import storage

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    storage.add_user(user.id, user.full_name, user.username)
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
        f"/status to start the bot \n" 
    )

async def my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Your Telegram ID: {update.effective_user.id}")

    # /start hello world
    # context.args # -> ["hello" "world"] 

async def order_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # /status 5  ->  context.args == ["5"]
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Использование: /status <номер заказа>\nНапример: /status 3")
        return

    order = storage.get_order(int(context.args[0]))
    # чужие заказы не показываем
    if order is None or order["user_id"] != update.effective_user.id:
        await update.message.reply_text("Заказ не найден 🤷")
        return

    await update.message.reply_text(
        f"Заказ №{order['id']}: {storage.STATUS_LABELS[order['status']]}"
    )