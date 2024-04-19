import random
import requests
import ast
from typing import List
import os

from databases.mongo_repository import database
from products.model import Clothes
from shopping_cart.model import ShoppingCart


def init_database():
    mongo_collections = database.list_collection_names()
    for collection in ["Clothes", "ShoppingCart"]:
        if collection in mongo_collections:
            database.drop_collection(collection)


def seed_clothes(number: int = 500):
    name = ["H&M", "Zara", "Uniqlo", "Forever 21", "Gap", "Old Navy", "Primark", "Topshop", "Mango",
            "ASOS", "Cotton On", "Urban Outfitters", "American Eagle", "Abercrombie & Fitch", "Express",
            "Forever New", "Pull&Bear", "New Look", "Boohoo", "River Island"]
    type = ["hat", "coat", "jacket", "shirt", "pants", "dress", "shoes", "socks", "gloves", "scarf"]
    colour = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "black", "white", "gray", "beige",
              "cyan", "magenta", "turquoise", "lavender", "maroon", "navy", "olive", "teal"]

    clothes_list = []
    for _ in range(number):
        random_name = random.choice(name)
        random_type = random.choice(type)
        random_colour = random.choice(colour)

        repeat_check = f"{random_name} {random_type} {random_colour}"
        if repeat_check in clothes_list:
            pass
        else:
            clothes = Clothes(name=random_name, type=random_type, colour=random_colour)
            clothes.create()
            print(f'Создан предмет одежды {_ + 1}')
            clothes_list.append(clothes)


def seed_shopping_cart(user_server_uri: str, shop_server_uri: str, number: int = 500):
    def get_user_id(start_pos: int = 0, limit: int = 100) -> int:

        headers = {
            'accept': 'application/json',
        }

        params = {
            'limit': str(limit),
            'start_pos': str(start_pos),
        }

        response = requests.get(f'{user_server_uri}/user/', params=params, headers=headers)
        users = ast.literal_eval(response.text)
        user_id = random.choice(users)['id']

        return user_id

    def get_product_ids(start_pos: int = 0, limit: int = 100) -> List[str]:
        headers = {
            'accept': 'application/json',
        }

        params = {
            'limit': str(limit),
            'start_pos': str(start_pos),
        }

        response = requests.get(f'{shop_server_uri}/clothes/', params=params, headers=headers)
        products = ast.literal_eval(response.text)

        products_num = random.randint(2, 10)

        product_ids = []
        for _ in range(products_num):
            product_id = random.choice(products)['_id']
            product_ids.append(product_id)

        return product_ids

    for _ in range(number):
        shopping_cart = ShoppingCart(user_id=get_user_id(start_pos=100, limit=10),
                                     product_ids=get_product_ids(start_pos=100, limit=10))
        shopping_cart.create()
        print(f'Создана корзина {_ + 1}')


init = 1
if init == 1:
    init_database()

seed_clothes()

user_server_uri = os.getenv("USER_URI")
shop_server_uri = os.getenv("SHOP_URI")
seed_shopping_cart(user_server_uri=user_server_uri, shop_server_uri=shop_server_uri)
