from fastapi import Header
from ..core.db  import db_cl
from ..rabbit.client import mq_cl
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession


async def get_session() -> AsyncSession: # type: ignore

    async_session = sessionmaker(
        db_cl.engine,
        class_=AsyncSession,
        expire_on_commit=True
    )

    async with async_session() as session:
        # return the db session
        yield session

        # close session so queue pool doesn't overflow
        await session.close()

async def get_current_user(x_forwarded_user: str = Header()) -> dict | None:
    user_id = int(x_forwarded_user)

    response = await mq_cl.send_rpc_message(
        "users.get_by_id", {
            "user_id": user_id
    })

    return response.get("data")

async def get_accommodation_by_id(accommodation_id: int) -> dict | None:
    response = await mq_cl.send_rpc_message(
        "accommodations.get_by_id", {
            "accommodation_id": accommodation_id
        }
    )

    return response.get("data")

async def get_user_accommodations(user_id: int) -> list | None:
    response = await mq_cl.send_rpc_message(
        "accommodations.get_by_user_id", {
            "user_id": user_id
        }
    )

    return response.get("data")