import jwt
from pydantic import ValidationError

from ..core.settings import ALGORITHM, SECRET_KEY
from ..models.user import User
from ..resources import strings


def get_user_from_token(token: str) -> User:
    try:
        return User(**jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub"))
    except jwt.PyJWTError as decode_error:
        raise ValueError(strings.UNABLE_JWT_TOKEN) from decode_error
    except ValidationError as validation_error:
        raise ValueError(strings.MALFORMED_TOKEN) from validation_error
