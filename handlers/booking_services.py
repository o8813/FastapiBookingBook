import httpx
from fastapi import HTTPException, status
from config import settings

async def get_object(url: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code not in (200, 201):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Error')

            if response.status_code == 404:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Page not found')

        except (KeyError, TypeError, ValueError):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Could not get credentials')

        return response.json()

async def get_hotel(hotel_id: int):
    url = f'{settings.booking_services_url}/hotels/{hotel_id}/'
    return await get_object(url=url)

async def get_room(room_id: int):
    url = f'{settings.booking_services_url}/rooms/{room_id}/'
    return await get_object(url=url)
