def booking_document_to_response(document: dict):
    return {
        'id': str(document['_id']),
        'user_id': document['user_id'],

        'hotel_id': document['hotel_id'],
        'hotel_name': document['hotel_name'],
        'room_id': document['room_id'],
        'room_number': document['room_number'],
        'room_price': document['room_price'],
        'checkin': document['checkin'],
        'checkout': document['checkout'],

        'total_price': document['total_price'],
        'status': document['status'],
        'created_date': document['created_date'],
        'updated_date': document['updated_date']
    }