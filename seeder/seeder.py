import ast
import os
import random

from faker import Faker
import requests

fake = Faker()


def clear_table(url: str, subj: str):
    headers = {
        'accept': 'application/json',
    }

    params = {
        'limit': '100',
    }

    check = [1]
    check_count = 1

    if (subj == 'user') or (subj == 'cart'):
        id_form = 'id'
    elif subj == 'clothes':
        id_form = '_id'

    while check:
        response = requests.get(f'{url}/{subj}/', params=params, headers=headers)
        entries_list = ast.literal_eval(response.text)
        entries_ids = []

        if len(entries_list) == 0:
            break

        print(f'Проверка {check_count}, найдено {len(entries_list)} записей из 100.')

        for _ in entries_list:
            entries_ids.append(_[id_form])

        for _ in entries_ids:
            requests.delete(f'{url}/{subj}/{_}', headers=headers)
            print(f'Удалена запись с id={_}...')

        check = entries_list
        check_count += 1


def seed_users(url: str, amount: int = 1000) -> str:
    not_created = 0

    for _ in range(amount):
        name = fake.first_name()
        surname = fake.last_name()
        nickname = fake.user_name()
        password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }

        json_data = {
            'name': name,
            'surname': surname,
            'nickname': nickname,
            'password': password,
        }

        response = requests.post(f'{url}/user/', headers=headers, json=json_data)

        if 'уже существует' in response.text:
            not_created += 1
        else:
            print(f"Создан пользователь: "
                  f"name: {name}, "
                  f"surname: {surname}, "
                  f"nickname: {nickname}, "
                  f"password: {password}...")

    return f'Создано {amount - not_created} пользователей, не создано - {not_created}.'


def seed_showcase(url: str, amount: int = 1000) -> str:
    not_created = 0
    clothes_list = []
    name = ["H&M", "Zara", "Uniqlo", "Forever 21", "Gap", "Old Navy", "Primark", "Topshop", "Mango",
            "ASOS", "Cotton On", "Urban Outfitters", "American Eagle", "Abercrombie & Fitch", "Express",
            "Forever New", "Pull&Bear", "New Look", "Boohoo", "River Island"]
    type = ["hat", "coat", "jacket", "shirt", "pants", "dress", "shoes", "socks", "gloves", "scarf"]
    colour = ["red", "orange", "yellow", "green", "blue", "purple", "pink", "brown", "black", "white", "gray", "beige",
              "cyan", "magenta", "turquoise", "lavender", "maroon", "navy", "olive", "teal"]

    for _ in range(amount):
        random_name = random.choice(name)
        random_type = random.choice(type)
        random_colour = random.choice(colour)

        repeat_check = f"{random_name} {random_type} {random_colour}"
        if repeat_check in clothes_list:
            not_created += 1
        else:
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json',
            }

            json_data = {
                'name': random_name,
                'type': random_type,
                'colour': random_colour,
            }

            response = requests.post(f'{url}/clothes/', headers=headers, json=json_data)

            print(f"Создан предмет одежды: "
                  f"name: {random_name}, "
                  f"type: {random_type}, "
                  f"colour: {random_colour}...")
            clothes_list.append(repeat_check)

    return f'Создано {amount - not_created} предметов одежды, не создано - {not_created}.'


def seed_carts(url: str, user_url: str, showcase_url: str, amount: int = 1000) -> str:
    def get_id(subj: str, url: str, start_pos: int = 0, limit: int = 100):
        headers = {
            'accept': 'application/json',
        }

        params = {
            'limit': str(limit),
            'start_pos': str(start_pos),
        }

        if subj == 'user':
            id_form = 'id'
        elif subj == 'clothes':
            id_form = '_id'

        response = requests.get(f'{url}/{subj}/', params=params, headers=headers)
        entries = ast.literal_eval(response.text)
        id = random.choice(entries)[id_form]

        return id

    for _ in range(amount):
        user_id = get_id(subj='user', url=user_url)
        product_id = get_id(subj='clothes', url=showcase_url)
        product_amount = random.randint(2, 10)

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }

        json_data = {
            'user_id': user_id,
            'product_id': product_id,
            'product_amount': product_amount,
        }

        response = requests.post(f'{url}/cart/', headers=headers, json=json_data)
        print(f"Создана запись корзины: "
              f"user_id: {user_id}, "
              f"product_id: {product_id}, "
              f"product_amount: {product_amount}...")

    return f'Создано {amount} записей корзины'


user_url = os.getenv("USER_URL")
user_subj = 'user'

showcase_url = os.getenv("SHOWC_URL")
showcase_subj = 'clothes'

cart_url = os.getenv("CART_URL")
cart_subj = 'cart'

clear = 0
if clear == 1:
    clear_table(url=user_url, subj=user_subj)
    clear_table(url=showcase_url, subj=showcase_subj)
    clear_table(url=cart_url, subj=cart_subj)

print(seed_users(url=user_url, amount=500))
print(seed_showcase(url=showcase_url, amount=500))
print(seed_carts(url=cart_url, user_url=user_url, showcase_url=showcase_url, amount=500))
