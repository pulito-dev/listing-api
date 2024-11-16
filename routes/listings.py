from .. import crud
from ..models import *
from .deps import get_db
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException


listings_router = APIRouter()


@listings_router.get("/")
async def get_all_listings(db: Session = Depends(get_db)) -> ListingsPublic:
    
    statement = select(Listing)
    listings = db.exec(statement).all()
    
    return ListingsPublic(data=listings)


@listings_router.get("/{id}")
async def get_accommodation_by_id(id: int, db: Session = Depends(get_db)) -> Listing:

    accommodation = db.get(Listing, id)

    if not accommodation:
        raise HTTPException(
            status_code=404,
            detail="No accommodation found with corresponding id"
        )

    return accommodation


@listings_router.post("/")
async def create_listing(create_listing: CreateListing, session: Session = Depends(get_db)) -> CreateListingPublic:
    listing = crud.create_listing(session, create_listing)

    return CreateListingPublic(
        id=listing.id,
        msg="Listing created successfully"
    )


@listings_router.patch("/{id}")
async def update_listing(id: int, update_listing: UpdateListing, session: Session = Depends(get_db)) -> UpdateListingPublic:
    listing = session.get(Listing, id)

    if not listing:
        raise HTTPException(
            status_code=404,
            detail=f"Listing with id {id} does not exist"
        )

    listing = crud.update_listing(session, listing, update_listing)

    return UpdateListingPublic(
        listing=listing,
        msg="Listing updated"
    )


@listings_router.delete("/id")
async def delete_listing(id: int, session: Session = Depends(get_db)) -> DeleteListingPublic:
    listing = session.get(Listing, id)

    if not listing:
        raise HTTPException(
            status_code=404,
            detail=f"Listing with id {id} does not exist"
        )
    
    crud.delete_listing(session, listing)

    return DeleteListingPublic(msg="Listing deleted successfully")
