import aiohttp
from starlette import status
from typing import Optional

from app.core.settings import TEAMS_URL
from app.models.teams import TeamForResponse


def verify_user(token: str) -> bool:
    url = f'{USERS_URL}/verify'
    async with aiohttp.ClientSession(headers={"Authorization": token}) as session:
        async with session.post(
                url
        ) as response:
            if response.status == status.HTTP_204_NO_CONTENT:
                return True
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN
            )
