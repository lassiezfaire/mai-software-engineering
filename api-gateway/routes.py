import json
import os

from circuitbreaker import circuit
from fastapi import APIRouter, HTTPException, status
import requests

router = APIRouter()

USER_URL = os.getenv('USER_URL')
SHOWC_URL = os.getenv('SHOWC_URL')
CART_URL = os.getenv('CART_URL')


@router.get("/", summary='Любой GET-запрос')
@circuit(failure_threshold=5, recovery_timeout=30)
def get_request(endpoint: str):
    service, request = endpoint.split('/')[0], endpoint.split('/')[1:]

    if service == 'user':
        url = USER_URL
    elif service == 'clothes':
        url = SHOWC_URL
    elif service == 'cart':
        url = CART_URL
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Нет такого сервиса')

    request = '/'.join(request)

    string = f'{url}/{service}/{request}'
    response = requests.get(string)
    beautified_string = json.loads(response.text)
    # print(string)

    return beautified_string


@router.post("/", summary='Любой POST-запрос')
@circuit(failure_threshold=5, recovery_timeout=30)
def post_request(endpoint: str, json_data: dict = {}):
    service, request = endpoint.split('/')[0], endpoint.split('/')[1:]

    if service == 'user':
        url = USER_URL
    elif service == 'clothes':
        url = SHOWC_URL
    elif service == 'cart':
        url = CART_URL
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Нет такого сервиса')

    request = ''.join(request)

    string = f'{url}/{service}/{request}'
    response = requests.post(string, json=json_data)

    beautified_string = json.loads(response.text)
    return beautified_string


@router.patch("/", summary='Любой PATCH-запрос')
@circuit(failure_threshold=5, recovery_timeout=30)
def patch_request(endpoint: str, json_data: dict = {}):
    service, request = endpoint.split('/')[0], endpoint.split('/')[1:]

    if service == 'user':
        url = USER_URL
    elif service == 'clothes':
        url = SHOWC_URL
    elif service == 'cart':
        url = CART_URL
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Нет такого сервиса')

    request = ''.join(request)

    string = f'{url}/{service}/{request}'
    response = requests.patch(string, json=json_data)

    beautified_string = json.loads(response.text)
    return beautified_string


@router.delete("/", summary='Любой DELETE-запрос')
@circuit(failure_threshold=5, recovery_timeout=30)
def delete_request(endpoint: str):
    service, request = endpoint.split('/')[0], endpoint.split('/')[1:]

    if service == 'user':
        url = USER_URL
    elif service == 'clothes':
        url = SHOWC_URL
    elif service == 'cart':
        url = CART_URL
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Нет такого сервиса')

    request = '/'.join(request)

    string = f'{url}/{service}/{request}'
    response = requests.delete(string)
    beautified_string = json.loads(response.text)

    return beautified_string
