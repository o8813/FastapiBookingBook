from fastapi import FastAPI, HTTPException, status
import uvicorn
from pymongo.errors import PyMongoError
from api.booking import router
from database.connection import connect_db, disconnect_db, get_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app_: FastAPI):
    try:
        await connect_db()
        print('Session connected')
        yield
    finally:
        await disconnect_db()
        print('Session closed')

app = FastAPI(title='Booking Book', lifespan=lifespan)
app.include_router(router)

@app.get('/')
async def test_db():
    return {'detail': 'Success'}

@app.get('/database')
async def check_db():
    try:
        database = get_db()
        await database.command('ping')
        return {'status': 'ok', 'database': database.name, 'connection': 'active'}
    except PyMongoError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error: Disconnected')

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, port=27018)