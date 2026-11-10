import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from config import BOT_TOKEN
from handlers import common, catalog

from keyboards import BTN_ABOUT, BTN_MY_ORDERS, BTN_CATALOG

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level= logging.INFO
)

def main () -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", common.start))
    app.add_handler(CommandHandler("help", common.help))
    app.add_handler(CommandHandler("myID", common.my_id))
    app.add_handler(CommandHandler("status", common.order_status))

    app.add_handler(MessageHandler(filters.Text(BTN_MY_ORDERS), common.my_orders))
    app.add_handler(MessageHandler(filters.Text(BTN_ABOUT), common.about))

    app.add_handler(MessageHandler(filters.Text([BTN_CATALOG]), catalog.show_catalog))

    print("Bot running ...")
    app.run_polling()

if __name__ == "__main__":
    main()