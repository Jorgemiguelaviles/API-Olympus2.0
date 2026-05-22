import os
import time
from jose import jwt
from dotenv import load_dotenv

load_dotenv()

PRIVATE_KEY_PATH = os.getenv("PRIVATE_KEY_PATH")

with open(PRIVATE_KEY_PATH, "r") as f:
    PRIVATE_KEY = f.read()

ALGORITHM = "RS256"
EXPIRE_MINUTES = 60


def create_access_token(data: dict):

    now = int(time.time())

    payload = data.copy()

    payload.update({
        "iat": now,
        "exp": now + EXPIRE_MINUTES * 60
    })

    token = jwt.encode(
        payload,
        PRIVATE_KEY,
        algorithm=ALGORITHM
    )

    return token


create_access_token({"sub": "user123"})