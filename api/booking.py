from fastapi import APIRouter, HTTPException, Depends, status
from database.schemes import BookingResponseScheme, BookingCreateScheme, BookingUpdateScheme, StatusChoices
from database.connection import get_collection
from database.mapper import booking_document_to_response
from handlers.booking_auth import get_current_user
from typing import Annotated, List
from handlers.booking_services import get_room, get_hotel
import asyncio
from datetime import datetime, time, timezone

router = APIRouter(prefix='/booking', tags=['Bookings'])

@router.get('/', response_model=List[BookingResponseScheme], tags=['Bookings'])
async def get_list(current_user: Annotated[dict, Depends(get_current_user)]):
    collection = get_collection()
    cursor = collection.find({'user_id': current_user['id']}).sort('created_date', -1)

    bookings = []

    async for i in cursor:
        bookings.append(booking_document_to_response(i))
    return bookings

@router.post('/', response_model=BookingResponseScheme, tags=['Booking'])
async def to_book(scheme: BookingCreateScheme, current_user: Annotated[dict, Depends(get_current_user)]):
    hotel, room = await asyncio.gather(get_hotel(scheme.hotel_id), get_room(scheme.room_id))
    if not hotel or not room:
        raise HTTPException(detail='Given room or hotel doesnt exists', status_code=status.HTTP_404_NOT_FOUND)

    checkin_datetime = datetime.combine(
        scheme.checkin,
        time.min,
        tzinfo=timezone.utc
    )

    checkout_datetime = datetime.combine(
        scheme.checkout,
        time.min,
        tzinfo=timezone.utc
    )

    # data_filter = {
    #     'room_id': scheme.room_id,
    #     'status': {
    #         '$in': [
    #             StatusChoices.pending.value,
    #             StatusChoices.confirmed.value
    #         ]
    #     },
    #     'checkin': {
    #         '$lt': checkout_datetime
    #     },
    #     'checkout': {
    #         '$gt': checkin_datetime
    #     }
    # }

    collection = get_collection()

    nights = (scheme.checkout - scheme.checkin).days
    room_price = float(room['price'])

    booking_document = {
        'user_id': current_user['id'],
        'hotel_id': scheme.hotel_id,
        'hotel_name': hotel['name'],
        'room_id': scheme.room_id,
        'room_number': room['room_number'],
        'room_price': room_price,
        'checkin': checkin_datetime.strftime('%Y-%m-%d'),
        'checkout': checkout_datetime.strftime('%Y-%m-%d'),
        'total_price': nights * room_price,
        'status': StatusChoices.confirmed.value,
        'created_date': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
        'updated_date': datetime.now(timezone.utc).strftime('%Y-%m-%d')
    }

    result = await collection.insert_one(booking_document)
    booking_document['_id'] = result.inserted_id

    return booking_document_to_response(booking_document)