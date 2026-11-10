import json
import os
import copy
from datetime import datetime

from config import DATA_FILE

DEFAULT_DB = {
    "users": {},
    "products": [],
    "orders": [],
    "next_product_id": 1,
    "next_order_id": 1,
}

STATUS_LABELS = {
    "new": "New",
    "accepted": "Accepted",
    "rejected": "Rejected",
}

""" --- basic / support Funcs """

def load_db() -> dict:
    if not os.path.exists(DATA_FILE):
        return copy.deepcopy(DEFAULT_DB)
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(db: dict) -> None:
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")



""" --- user """

def add_user(user_id: int, name: str, username: str | None):
    db = load_db()
    key = str(user_id)
    if key not in db["users"]:
        db["users"][key] = {
            "name": name,
            "username": username,
            "joinedAt": now()
        }

        save_db(db)

def get_all_user_ids() -> list[int]:
    return [int(uid) for uid in load_db()["users"]] 

    # result = []
    # for uid in load_db["users"]:
    #     result.append(int(uid))

    # return result

""" --- product"""

def add_product(name: str, price: int, desc: str, photo_id: str | None) -> dict:
    db = load_db()
    product = {
        "id": db["next_product_id"],
        "name": name,
        "price": price,
        "description": desc,
        "photo_id": photo_id
    } 

    db["products"].append(product)
    db["next_product_id"] += 1
    save_db(db)
    return product

def get_products() -> list[dict]: return load_db()["products"]

def get_product(product_id: int): 
    return next((p for p in get_products() if p["id"] == product_id), None)

    # for product in get_products():
    #     if product["id"] == product_id:
    #         return product
    # return None
    
def delete_product(product_id: int) -> bool:
    db = load_db
    before = len(db["products"])
    db["products"] = [ p for p in db["products"] if p["id"] != product_id ]

    # result = []
    # for p in db["products"]:
    #     if p["id"] !=  product_id:
    #         result.append(p)

    save_db(db)
    return len(db["products"]) < before

def seed_demo_products():
    if get_products: return 

    add_product("Shirt", 150, "Blue tshirt", None)
    add_product("Cap", 50, "Red cap", None)
    add_product("Shoes", 200, "Black shoes", None)


""" --- orders"""

def add_order(user_id: int, product: dict, quantity: int,
              name: str, phone: str, address: str) -> dict:
    db = load_db()
    order = {
        "id": db["next_order_id"],
        "user_id": user_id,
        "product_id": product["id"],
        "product_name": product["name"],  # копируем: товар могут удалить
        "quantity": quantity,
        "total": product["price"] * quantity,
        "name": name,
        "phone": phone,
        "address": address,
        "status": "new",
        "created": now(),
    }
    db["orders"].append(order)
    db["next_order_id"] += 1
    save_db(db)
    return order


def get_order(order_id: int) -> dict | None:
    return next((o for o in load_db()["orders"] if o["id"] == order_id), None)


def get_orders(status: str | None = None) -> list[dict]:
    orders = load_db()["orders"]
    return [o for o in orders if status is None or o["status"] == status]


def get_user_orders(user_id: int) -> list[dict]:
    return [o for o in load_db()["orders"] if o["user_id"] == user_id]


def set_order_status(order_id: int, status: str) -> dict | None:
    db = load_db()
    for order in db["orders"]:
        if order["id"] == order_id:
            order["status"] = status
            save_db(db)
            return order
    return None