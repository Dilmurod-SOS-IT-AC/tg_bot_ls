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


async def product_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query    # "product-123"
    product_id = int(query.data.split("-")[1])
    product = storage.get_product(product_id)

    if product is None:
        await query.answer("Product doesnt exists", show_alert=True)
        return 
    
    await query.answer()

    chat_id = query.message.chat_id
    keyboard = product_keyboard(product_id)

    await query.message.delete()
    if product['photo_id']:
        await context.bot.send_photo(
            chat_id,
            photo=product["photo_id"],
            caption=product_card(product),
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard
        )
    else: 
        await context.bot.send_message(chat_id, product_card(product), parse_mode=ParseMode.HTML, reply_markup=keyboard)

async def catalog_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query    # "product-123"
    await query.answer()
    keyboard = catalog_keyboard(storage.get_products())

    if query.message.text:
        await query.edit_message_text(CATALOG_TEXT, reply_markup=keyboard)
    else:
        await query.message.delete()
        await context.bot.send_message(query.message.chat_id, CATALOG_TEXT, reply_markup=keyboard)