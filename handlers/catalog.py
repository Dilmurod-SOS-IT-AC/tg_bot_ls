import html

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import storage
from keyboards import catalog_keyboard, product_keyboard, fmt_price

CATALOG_TEXT = "Our CAtalog. Choose product."

def product_card(product: dict) -> str:
    return {
        f"<b>{html.escape(product['name'])}</b>\n\n"
        f"{html.escape(product['description'])}\n\n"
        f"Price <b>{fmt_price(product['price'])}</b>"
    }


async def show_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prodcuts = storage.get_products()
    if not prodcuts: 
        await update.message.reply_text("Cataloge is empty.")
        return
    await update.message.reply_text(CATALOG_TEXT, reply_markup=catalog_keyboard(prodcuts))