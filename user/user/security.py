import bcrypt
import jwt


def hash_password(password: str) -> bytes:
    password_bytes = str.encode(password, encoding='utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


def check_password(password: str, hashed_password: str) -> bool:
    hashed_password = str.encode(hashed_password)
    print(hashed_password)
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)


def check_jwt(token: str, secret_key: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return "Токен устарел"
    except jwt.InvalidTokenError:
        return "Токен недействителен"
