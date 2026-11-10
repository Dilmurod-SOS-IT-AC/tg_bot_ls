import re

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, filters

import storage
from keyboards import BTN_CANCEL, main_menu, fmt_price

CANCEL_FILTER = filters.Regex(f"^{re.escape(BTN_CANCEL)}")
TEXT_INPUT = filters.TEXT & ~filters.COMMAND & ~CANCEL_FILTER

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    storage.add_user(user.id, user.full_name, user.username)
    await update.message.reply_text(
        f"Hello, {user.first_name} \n"
        f"Welcome to the ShopBot",
        reply_markup= main_menu()
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

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ShopBot - bla bla bla"
    )

    await update.message.reply_location(latitude=41.3111, longitude=40.1234)

async def my_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    orders = storage.get_user_orders(update.effective_user.id)

    if not orders:
        await update.message.reply_text("U dont have any orders yet.")
        return

    lines = ["Your Orders:\n"]
    for o in orders[-10]:
        lines.append(
            f"#{o['id'] - {o['product_name']} - {o['quantity']}} ."
            f"#{fmt_price(o['total'])} - {storage.STATUS_LABELS[o['status']]} ."
        )
    await update.message.reply_text('\n'.join(lines))

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.effective_message.reply_text("Action canceled", reply_markup=main_menu())
    return ConversationHandler.END


async def unknown_text(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    await update.message.reply_text("Unknown text.")

async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    await update.message.reply_text("Unknown command.")