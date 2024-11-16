from .models import *
from sqlmodel import Session, select
from datetime import datetime


def get_listings_in_timeframe(session: Session, dt_from: datetime, dt_to: datetime):
    pass


def create_listing(session: Session, listing_create: CreateListing) -> Listing:
    listing = Listing.model_validate(
        listing_create
    )
    session.add(listing)
    session.commit()
    session.refresh(listing)

    return listing


def update_listing(session: Session, db_listing: Listing, listing_update: UpdateListing) -> Listing:
    new_data = listing_update.model_dump(exclude_unset=True)
    db_listing.sqlmodel_update(
        new_data
    )
    session.add(db_listing)
    session.commit()
    session.refresh(db_listing)

    return db_listing

def delete_listing(session: Session, db_listing: Listing):
    session.delete(db_listing)
    session.commit()