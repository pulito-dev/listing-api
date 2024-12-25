from sqlmodel import Session, create_engine, SQLModel
# TODO: make sure all models are imported here so sqlmodel can form the relationships
from ..models import *

class DBClient():
    def __init__(self):
        self.engine = None
        
    def connect(self, uri: str, connect_args: dict = {}):
        self.engine = create_engine(
            url=uri,
            connect_args=connect_args,
            # check for conn liveliness before checkout
            pool_pre_ping=True,
            # recycle idle connections younger than 10 mins
            pool_recycle=600
        )

    def init_db(self):
        SQLModel.metadata.create_all(self.engine)
    
    def disconnect(self):
        self.engine.dispose()
        self.engine = None


db_cl = DBClient()