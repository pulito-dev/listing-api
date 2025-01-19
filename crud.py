from .models import *
from datetime import datetime
from sqlmodel import select, col, delete
from sqlalchemy.ext.asyncio.session import AsyncSession


def get_listings_in_timeframe(session: AsyncSession, dt_from: datetime, dt_to: datetime):
    pass


async def get_user_listings(session: AsyncSession, accommodation_ids: list[int]) -> list[Listing]:
    statement = select(Listing).where(col(Listing.accommodation_id).in_(accommodation_ids))

    res = await session.execute(statement)

    listings = res.scalars().all()

    return listings

async def create_listing(session: AsyncSession, listing_create: CreateListing) -> Listing:
    listing = Listing.model_validate(
        listing_create
    )
    session.add(listing)
    await session.commit()
    await session.refresh(listing)

    return listing


async def update_listing(session: AsyncSession, db_listing: Listing, listing_update: UpdateListing) -> Listing:
    new_data = listing_update.model_dump(exclude_unset=True)
    db_listing.sqlmodel_update(
        new_data
    )
    session.add(db_listing)
    await session.commit()
    await session.refresh(db_listing)

    return db_listing

async def delete_listing(session: AsyncSession, db_listing: Listing):
    await session.delete(db_listing)
    await session.commit()
