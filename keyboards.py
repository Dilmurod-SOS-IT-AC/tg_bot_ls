from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup
)

BTN_CATALOG = "Catalog"
BTN_MY_ORDERS = "My Orders"
BTN_ABOUT = "About"
BTN_CANCEL = "Cancel"
BTN_FEEDBACK = "Feendback"



def fmt_price(value: int) -> str: 
    return f"{value:.}".replace(".", " ") + " som"

def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [BTN_CATALOG, BTN_MY_ORDERS],
            [BTN_FEEDBACK, BTN_ABOUT]
        ],
        resize_keyboard=True,
        input_field_placeholder="Choose menu item."
    ) 

def cancel_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup([[BTN_CANCEL]], resize_keyboard=True)

def phone_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("Send number", request_contact=True)],
            [BTN_CANCEL]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )



def catalog_keyboard(products: list[dict]) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(
            f"{p['name']} - {fmt_price(p['price'])}",
            callback_data=f"product:{p['id']}"
        )]
        for p in products
    ]
    return InlineKeyboardMarkup(rows)

def product_keyboard(product_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Order", callback_data=f"order:{product_id}")]
        [InlineKeyboardButton("Back", callback_data=f"catalog")]
    ])