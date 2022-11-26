from bcrypt import checkpw, hashpw

# SALT_KEY=gensalt()
SALT_KEY = b"$2b$12$C7d8F1zsAN7BPTcR1KzIru"


def check_password(password: str, hashed_password: str) -> bool:
    return checkpw(password.encode(), hashed_password.encode())


def hash_password(password: str) -> str:
    return hashpw(password.encode(), SALT_KEY).decode()
