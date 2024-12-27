from .. import crud
from ..models import *
from .deps import get_session
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession


listings_router = APIRouter()


@listings_router.get("/")
async def get_all_listings(session: AsyncSession = Depends(get_session)) -> ListingsPublic:
    
    statement = select(Listing)
    res = await session.execute(statement)
    listings = res.scalars().all()
    
    return ListingsPublic(data=listings)


@listings_router.get("/{id}")
async def get_accommodation_by_id(id: int, session: Session = Depends(get_session)) -> Listing:

    accommodation = await session.get(Listing, id)

    if not accommodation:
        raise HTTPException(
            status_code=404,
            detail="No accommodation found with corresponding id"
        )

    return accommodation


@listings_router.post("/")
async def create_listing(create_listing: CreateListing, session: Session = Depends(get_session)) -> CreateListingPublic:
    listing = await crud.create_listing(session, create_listing)

    return CreateListingPublic(
        id=listing.id,
        msg="Listing created successfully"
    )


@listings_router.patch("/{id}")
async def update_listing(id: int, update_listing: UpdateListing, session: Session = Depends(get_session)) -> UpdateListingPublic:
    listing = await session.get(Listing, id)

    if not listing:
        raise HTTPException(
            status_code=404,
            detail=f"Listing with id {id} does not exist"
        )

    listing = await crud.update_listing(session, listing, update_listing)

    return UpdateListingPublic(
        listing=listing,
        msg="Listing updated"
    )


@listings_router.delete("/id")
async def delete_listing(id: int, session: Session = Depends(get_session)) -> DeleteListingPublic:
    listing = await session.get(Listing, id)

    if not listing:
        raise HTTPException(
            status_code=404,
            detail=f"Listing with id {id} does not exist"
        )
    
    await crud.delete_listing(session, listing)

    return DeleteListingPublic(msg="Listing deleted successfully")
