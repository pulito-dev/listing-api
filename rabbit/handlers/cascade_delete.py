import json
from ..client import mq_cl
from ...models import Listing
from sqlmodel import col, delete
from aio_pika import IncomingMessage
from ...routes.deps import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession

async def cascade_delete_handler(msg: IncomingMessage):
    # if an exception gets raised, message gets rejected and put back in the queue
    async with msg.process(requeue=True):
        msg_body = json.loads(
            msg.body.decode()
        )

        accommodation_id = msg_body.get("accommodation_id")

        # open session
        session_gen = get_session()
        session: AsyncSession = await anext(session_gen)

        # start transaction
        session.begin()
        try:
            if isinstance(accommodation_id, int):
                statement = delete(Listing).where(
                    Listing.accommodation_id==accommodation_id
                )
            elif isinstance(accommodation_id, list):
                statement = delete(Listing).where(
                    col(Listing.accommodation_id).in_(accommodation_id)
                )
            else:
                raise Exception()

            await session.execute(statement)
            # raise Exception("SIMULATING ERROR")
        except:
            await session.rollback()
            await mq_cl.send_rpc_response("listings.cascade_delete",
                {
                    "success": False,
                    "msg": f"Something went wrong."
                },
                msg.correlation_id
            )
        else:
            await session.commit()
            # respond to callback queue
            await mq_cl.send_rpc_response("listings.cascade_delete",
                {
                    "success": True,
                    "msg": f"Successfully deleted listings with accommodation id {accommodation_id}"
                },
                msg.correlation_id
            )

