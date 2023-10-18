from datetime import datetime, timedelta, timezone
import os
import jwt
from dotenv import load_dotenv
from .cache import cache


load_dotenv()
jwt_secret = os.getenv("JWT_SECRET_KEY")


def encode_jwt(payload: dict[str, str]) -> str:
    return jwt.encode(payload, jwt_secret, algorithm="HS256")


def decode_token(token) -> str:
    token_data = jwt.get_unverified_header(token)

    payload = jwt.decode(
        token,
        key=jwt_secret,
        algorithms=[token_data['alg'], ],
        options={"require": ["exp", "sub"]}
    )
    print('payload', payload)
    return payload['sub']


def create_token() -> tuple[int, str]:
    id = cache.get_next_id()
    print(id)
    return id, encode_jwt({
        'sub': id,
        'exp': int((datetime.now(tz=timezone.utc) + timedelta(hours=1)).timestamp())
    })
