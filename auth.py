from jose import jwt, JWTError

SECRET_KEY = "my-super-secret-key"
ALGORITHM = "HS256"

def create_access_token(username: str):

    data = {
        "sub": username
    }
    token = jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=ALGORITHM
        )
        username = payload.get("sub")

        if username is None:
            return None

        return username
    except JWTError:
        return None

