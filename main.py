from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.db_manager import db, initialize_db
from api.api_v1.api import authentication_router
import uvicorn


@asynccontextmanager
async def lifespan(application: FastAPI):
    initialize_db()
    yield
    if not db.is_closed():
        db.close()


app = FastAPI(lifespan=lifespan)

app.include_router(authentication_router, tags=['authentication'] ,prefix='/authentication')


# uvicorn.run(app=app, host='127.0.0.1', port=8001)