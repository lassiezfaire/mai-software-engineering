import jwt


def check_jwt(token: str, secret_key: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return "Токен устарел"
    except jwt.InvalidTokenError:
        return "Токен недействителен"
