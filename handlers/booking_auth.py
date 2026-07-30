import httpx
from config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated

async def verify_access_token(token: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f'{settings.booking_auth_url}/profile/',
                headers={'Authorization': f'Bearer {token}'}
            )

        except httpx.RequestError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Could not connect to auth service')

        if response.status_code == 401:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or expired token')

        try:
            user_data = response.json()
            return {
                'id': int(user_data['id']),
                'username': user_data['username'],
                'status': user_data['status']
            }

        except (KeyError, TypeError, ValueError):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Could not get credentials')

bearer_scheme = HTTPBearer(auto_error=False)
async def get_current_user(
        credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)]
):
    if credentials is None:
        raise HTTPException(detail='Authentication credentials were not provided', status_code=status.HTTP_401_UNAUTHORIZED)

    elif credentials.scheme.lower() != 'bearer':
        raise HTTPException(detail='Token type is not Bearer', status_code=status.HTTP_401_UNAUTHORIZED)

    return await verify_access_token(credentials.credentials)