from fastapi import HTTPException
import sqlalchemy as sql
import sqlalchemy.orm as orm
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from pydantic import BaseModel

# Database URI.
SQLALCHEMY_DATABASE_URL = "sqlite:///./marketplace.db"

engine = sql.create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()


SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)


# DTOs
class Listings(BaseModel):
    name:str
    description:str
    price: int
    
class ListingCreate(Listings):
        pass
    
class Listing(Listings):
    id:int
    class Config:
        orm_mode =True
        
        
        
# Table
class ListingModel(Base):
    
    __tablename__ = "listings"
    id = Column(Integer, primary_key= True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    
    @staticmethod
    def get_listings(db: Session):
        return db.query(ListingModel).all()
    
    @staticmethod
    def create_listing(db:Session, listing:ListingCreate):
        """Insert an listing in the database"""
        the_listing = ListingModel(**listing.dict())
        db.add(the_listing)
        db.commit()
        return the_listing
    
    
    @staticmethod
    def update_listing(db:Session, id:int, listing:ListingCreate):
        """update listing details"""
        the_listing:Listing = db.query(ListingModel).filter(ListingModel.id==id).first()
        if the_listing is None:
            raise HTTPException(status_code=404, detail="Listing not found")
        the_listing.name = listing.name
        the_listing.description = listing.description
        the_listing.price = listing.price
        db.commit()
        return the_listing
    

    @staticmethod
    def get_listing(listing_id:int, db:Session):
        """return an listing that matches the id provided"""
        return db.query(ListingModel).filter(ListingModel.id==listing_id).first()