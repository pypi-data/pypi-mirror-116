from starlette.config import Config
from starlette.datastructures import Secret


config = Config(".env")


SECRET_KEY = config("SECRET_KEY", cast=Secret, default="SUPERSECRETKEYIFYOUKNOWWHATIMEAN")
JWT_SUBJECT = 'access'
ALGORITHM = 'HS256'
USERS_URL = config("USERS_URL", cast=str, default="https:users.dev-bayestech.ru/public/v1/verify")
