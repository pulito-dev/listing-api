from decimal import Decimal
from .core.config import config
from datetime import datetime, UTC
from sqlmodel import Field, SQLModel


# base model for all models
# makes sure that all models are created in the appropriate schema
class BaseModel(SQLModel):
    __table_args__ = {"schema": str(config.DB_SCHEMA)}


# request models
# todo: add rule to strip and check empty strings https://stackoverflow.com/a/70262769/10513667
# todo: add a base model for inheriting common fields


class CreateListing(BaseModel):
    # TODO: add a validator for `payout >= 20.00`
    payout: Decimal = Field(default=20.00, max_digits=6, decimal_places=2)
    # TODO: add a validator for `to_be_cleaned_from >= datetime.now()`
    to_be_cleaned_from: datetime | None
    # TODO: add a validator for `before - from >= 1 hour`
    # TODO: add a validator for `to_be_cleaned_before >= datetime.now()`
    to_be_cleaned_before: datetime | None
    description: str | None

    accommodation_id: int


class UpdateListing(BaseModel):
    # TODO: add a validator for `payout >= 20.00`
    payout: Decimal = Field(default=20.00, max_digits=6, decimal_places=2)
    # TODO: add a validator for `to_be_cleaned_from >= datetime.now()`
    to_be_cleaned_from: datetime | None
    # TODO: add a validator for `before - from >= 1 hour`
    # TODO: add a validator for `to_be_cleaned_before >= datetime.now()`
    to_be_cleaned_before: datetime | None
    description: str | None


# db models


class Listing(BaseModel, table=True):
    id: int = Field(primary_key=True, default=None)
    payout: Decimal = Field(default=20.00, max_digits=6, decimal_places=2)
    to_be_cleaned_from: datetime | None
    to_be_cleaned_before: datetime | None
    description: str | None
    posted_on: datetime | None = Field(default_factory=lambda: datetime.now(UTC))

    accommodation_id: int


# response models
    
class ListingsPublic(BaseModel):
    data: list[Listing]


class CreateListingPublic(BaseModel):
    id: int
    msg: str


class UpdateListingPublic(BaseModel):
    listing: Listing
    msg: str


class DeleteListingPublic(BaseModel):
    msg: str
