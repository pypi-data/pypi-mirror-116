from typing import Callable, List, Optional

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from starlette import status

from bt_auth.resources import strings
from ..models.user import User
from ..resources.enums import UserStatus
from ..services.jwt import get_user_from_token
from ..services.users import verify_user

api_key_header = APIKeyHeader(name='Authorization')


async def _verify_token(authorization: str = Depends(api_key_header)):
    await verify_user(authorization)
    try:
        token_prefix, token = authorization.split()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.WRONG_TOKEN_FORMAT,
        )
    if token_prefix != 'Bearer':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.WRONG_TOKEN_PREFIX,
        )
    return token


async def _get_user(token: str = Depends(_verify_token)) -> User:
    try:
        return await get_user_from_token(token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


async def get_current_user(
        statuses: List[UserStatus]
) -> Callable[[User], User]:
    def _get_accepted_user(user: User = Depends(_get_user)) -> User:
        if user.status not in statuses:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        verify_user()
        return user
    return _get_accepted_user
