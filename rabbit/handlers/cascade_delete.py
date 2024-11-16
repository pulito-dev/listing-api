import json
from sqlmodel import Session
from ...models import Listing
from ...core.db import db_cl
from sqlalchemy import delete
from aio_pika import IncomingMessage

async def cascade_delete_handler(msg: IncomingMessage):
    # if an exception gets raised, message gets rejected and put back in the queue
    async with msg.process(requeue=True):
        msg_body = json.loads(
            msg.body.decode()
        )

        accommodation_id = msg_body["accommodation_id"]

        # cascade delete all the listings with corresponding id
        with Session(db_cl.engine) as session:
            statement = delete(Listing).where(
                Listing.accommodation_id==accommodation_id
            )
            session.exec(statement)
            session.commit()
