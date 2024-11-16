from .core.db import db_cl
from fastapi import FastAPI
from .core.config import config
from .rabbit.client import mq_cl
from contextlib import asynccontextmanager
from sqlalchemy.schema import CreateSchema

from .rabbit.handlers.cascade_delete import cascade_delete_handler


@asynccontextmanager
async def lifespan(_: FastAPI):
    # everything before yield is executed before the app starts up
    # set up rabbit
    await mq_cl.connect(str(config.RABBIT_URI))
    await mq_cl.consume("listings.cascade_delete", cascade_delete_handler)
    # await mq_cl.consume("listings.asdf

    # set up db
    db_cl.connect(str(config.DB_URI))
    with db_cl.engine.connect() as conn:
        conn.execute(CreateSchema(str(config.DB_SCHEMA), if_not_exists=True))
        conn.commit()

    # create tables
    db_cl.init_db()

    yield
    
    # everything after yield is execute after the app shuts down
    await mq_cl.disconnect()
    db_cl.disconnect()


app = FastAPI(
    title=config.TITLE,
    lifespan=lifespan
)


from .routes.listings import listings_router


app.include_router(listings_router, prefix="/listings")


# @app.api_route("/")
# async def home():
#     txt = "".join(random.choices(string.ascii_letters, k=4))
#     await mq_cl.send_message("accommodations", {
#         "random_id": txt
#     })
#     print(f"SENT: {txt}")

#     return {
#         "hello": "world"
#     }
