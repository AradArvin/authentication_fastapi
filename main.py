from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from db.db_manager import db, initialize_db
from api.api_v1.api import authentication_router
from core.settings import DEBUG



@asynccontextmanager
async def lifespan(application: FastAPI):
    initialize_db()
    yield
    if not db.is_closed():
        db.close()

app = FastAPI(lifespan=lifespan)

allowed_hosts = []
if DEBUG:
    allowed_hosts.extend(['localhost', '127.0.0.1'])
app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

app.include_router(authentication_router, tags=['authentication'] ,prefix='/authentication')


# uvicorn.run(app=app, host='127.0.0.1', port=8001)