import logging

from telegram import Update
from telegram.ext import Application, CommandHandler

from config import BOT_TOKEN
from handlers import common

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
    
    print("Bot running ...")
    app.run_polling()

if __name__ == "__main__":
    main()