from datetime import datetime, timedelta
from time import time
from typing import Optional

import jwt
from bcrypt import checkpw, hashpw
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.container import AppContainer
from app.core.conf import AppConf
from app.core.exceptions import UnAuthorized

# SALT_KEY=gensalt()
SALT_KEY = b'$2b$12$C7d8F1zsAN7BPTcR1KzIru'


def check_password(password: str, hashed_password: str) -> bool:
    return checkpw(password.encode(), hashed_password.encode())


def hash_password(password: str) -> str:
    return hashpw(password.encode(), SALT_KEY)


def sign_jwt(user_id: int, secret: str):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
        'sub': str(user_id)
    }
    return jwt.encode(payload, secret, algorithm='HS256')


def decode_jwt(token: str, secret: str) -> Optional[int]:
    try:
        decoded = jwt.decode(token, secret, algorithms='HS256')
        if decoded["exp"] < time():
            return None

        user_id = int(decoded['sub'])
        return user_id
    except Exception as e:
        print("Exp {}", e)
        return None


security = HTTPBearer()


@inject
def get_current_user(
    credentials:  HTTPAuthorizationCredentials = Security(security),
    app: AppConf = Depends(Provide[AppContainer.app_conf]),
) -> int:
    if credentials.credentials == '':
        raise UnAuthorized()

    user_id = decode_jwt(credentials.credentials, app.jwt_secret)
    if not user_id:
        raise UnAuthorized()

    return user_id
