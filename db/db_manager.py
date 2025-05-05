from peewee import *
from datetime import datetime, timezone

db = SqliteDatabase('authentication.db')


class BaseModel(Model):
    id = AutoField()
    class Meta:
        database = db


class UserData(BaseModel):
    username = TextField(unique=True)
    password = TextField()
    email = TextField()
    full_name = TextField(null=True)
    role = TextField()
    join_date = DateTimeField(default=datetime.now(timezone.utc))
    is_active = BooleanField(default=True)

    class Meta:
        table_name = 'UserData'


def initialize_db():
    db.connect()
    db.create_tables([UserData,])


def get_db():
    try:
        db.connect()
        yield db
    finally:
        if not db.is_closed():
            db.close()
