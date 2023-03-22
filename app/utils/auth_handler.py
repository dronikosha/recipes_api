import os
from dotenv import load_dotenv
import time
from typing import Dict
from ..schemas import AdminSchema

import jwt

load_dotenv()


admin_login = os.getenv("ADMIN_LOGIN")
admin_pwd = os.getenv("ADMIN_PASSWORD")
JWT_SECRET = os.getenv("SECRET_TOKEN")
JWT_ALGORITHM = "HS256"


def token_response(token: str):
    return {
        "access_token": token
    }
    
    
def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
    
    
def check_user(data: AdminSchema):
    if admin_login == data.login and admin_pwd == data.password:
        return True
    return False