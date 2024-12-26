from ..models import *
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine

class DBClient():
    def __init__(self):
        self.engine = None
        
    def connect(self, uri: str, connect_args: dict = {}):
        self.engine = create_async_engine(
            url=uri,
            connect_args=connect_args,
            # check for conn liveliness before checkout
            pool_pre_ping=True,
            # recycle idle connections younger than 30 mins
            pool_recycle=1800,
            # connection pool size
            pool_size=50,
            # pool overflow size
            max_overflow=75
        )

    def init_db(self):
        SQLModel.metadata.create_all(self.engine)
    
    def disconnect(self):
        self.engine.dispose()
        self.engine = None


db_cl = DBClient()