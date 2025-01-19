from .. import crud
from ..models import *
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
from .deps import get_session, get_current_user, get_accommodation_by_id, get_user_accommodations


listings_router = APIRouter()


@listings_router.get("/")
async def get_all_listings(session: AsyncSession = Depends(get_session))  -> ListingsPublic:
    
    statement = select(Listing)
    res = await session.execute(statement)
    listings = res.scalars().all()
    
    return ListingsPublic(data=listings)


@listings_router.get("/my")
async def get_user_listings(session: Session = Depends(get_session), current_user: dict = Depends(get_current_user)) -> ListingsPublic:
    accommodation_ids = await get_user_accommodations(current_user.get("id"))
    
    listings = await crud.get_user_listings(session, accommodation_ids)
    
    return ListingsPublic(data=listings)


@listings_router.get("/{id}")
async def get_listing_by_id(id: int, session: Session = Depends(get_session)) -> Listing:

    listing: Listing = await session.get(Listing, id)

    if not listing:
        raise HTTPException(
            status_code=404,
            detail="No listing found with corresponding id"
        )
    
    return listing


@listings_router.post("/")
async def create_listing(create_listing: CreateListing, session: Session = Depends(get_session), current_user: dict = Depends(get_current_user)) -> CreateListingPublic:

    accommodation: dict = await get_accommodation_by_id(create_listing.accommodation_id)

    if not accommodation:
        raise HTTPException(
            status_code=404,
            detail=f"Accommodation with id {create_listing.accommodation_id} does not exist"
        )
    
    # check if accommodation belongs to user
    if accommodation.get("user_id") != current_user.get("id"):
        raise HTTPException(
            status_code=403,
            detail="This accommodation does not belong to you"
        )

    listing = await crud.create_listing(session, create_listing)

    return CreateListingPublic(
        id=listing.id,
        msg="Listing created successfully"
    )


@listings_router.patch("/{id}")
async def update_listing(id: int, update_listing: UpdateListing, session: Session = Depends(get_session), current_user: dict = Depends(get_current_user)) -> UpdateListingPublic:

    listing: Listing = await session.get(Listing, id)

    if not listing:
        raise HTTPException(
            status_code=404,
            detail=f"Listing with id {id} does not exist"
        )
    
    accommodation = await get_accommodation_by_id(listing.accommodation_id)

    # check if user is his own listing
    if accommodation.get("user_id") != current_user.get("id"):
        raise HTTPException(
            status_code=403,
            detail=f"You cannot edit this listing"
        )

    listing = await crud.update_listing(session, listing, update_listing)

    return UpdateListingPublic(
        listing=listing,
        msg="Listing updated"
    )


@listings_router.delete("/{id}")
async def delete_listing(id: int, session: Session = Depends(get_session), current_user: dict = Depends(get_current_user)) -> DeleteListingPublic:
    listing: Listing = await session.get(Listing, id)

    if not listing:
        raise HTTPException(
            status_code=404,
            detail=f"Listing with id {id} does not exist"
        )
    
    accommodation = await get_accommodation_by_id(listing.accommodation_id)

    # check if user is his own listing
    if accommodation.get("user_id") != current_user.get("id"):
        raise HTTPException(
            status_code=403,
            detail=f"You cannot delete this listing"
        )
    
    await crud.delete_listing(session, listing)

    return DeleteListingPublic(msg="Listing deleted successfully")
