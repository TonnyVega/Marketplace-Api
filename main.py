from typing import List
from fastapi import Depends, FastAPI, HTTPException
import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from models import *

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title = 'Marketplace App',
    description='An api that handles sales and purchases',
    version='1.0.0'
)
# Middleware CORS

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#   Dependancy 
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        
Base.metadata.create_all(engine)


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
        

#Routes
@app.get('/')
def home():
    return {"api":"Marketplace"}

@app.get('/listings',status_code=200,response_model=List[Listing])
async def listings(db:Session = Depends(get_db) ):
    listings = ListingModel.get_listings(db=db)
    return  listings


@app.get('/listing/{listing_id}', response_model=Listing)
async def listing(listing_id:int,  db:Session = Depends(get_db)):
    the_listing = ListingModel.get_listing(db=db,listing_id=listing_id)
    if  the_listing is None:
        raise HTTPException(status_code=404, detail="The listing does not exist")
    return  the_listing


@app.post('/listings',status_code=201,response_model=Listing)
async def create_listings(listing:ListingCreate, db: Session = Depends(get_db)):
    return ListingModel.create_listing(db=db, listing=listing)

@app.put('/listings/{listing_id}',status_code=200,response_model=Listing)
async def update_listing(Listing:ListingCreate, listing_id:int, db:Session = Depends(get_db)):
    return ListingModel.update_listing(id=listing_id,listing=Listing,db=db)




