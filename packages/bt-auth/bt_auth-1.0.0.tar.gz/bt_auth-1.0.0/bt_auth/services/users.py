import requests
from starlette import status
from fastapi import Depends, HTTPException
from typing import Optional

from ..core.settings import USERS_URL


def verify_user(token: str) -> bool:
    url = f'{USERS_URL}/verify'
    with requests.Session() as session:
        with session.post(
            url,
            headers={"Authorization": token}
        ) as response:
            if response.status_code == status.HTTP_204_NO_CONTENT:
                return True
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN
                )
