
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Kisaan Setu API",
    description="Crop price discovery and farmer-buyer market links",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Synthetic demo data only — not live mandi prices.
crop_prices = [
    {"id": 1, "crop": "Potato", "market": "Jalpaiguri",
     "price": 1450, "demand": "High"},
    {"id": 2, "crop": "Potato", "market": "Medinipur",
     "price": 1520, "demand": "Medium"},
    {"id": 3, "crop": "Tomato", "market": "Jalpaiguri",
     "price": 2300, "demand": "High"},
    {"id": 4, "crop": "Tomato", "market": "Medinipur",
     "price": 2150, "demand": "Medium"},
    {"id": 5, "crop": "Onion", "market": "Jalpaiguri",
     "price": 2600, "demand": "Medium"},
    {"id": 6, "crop": "Onion", "market": "Medinipur",
     "price": 2725, "demand": "High"},
    {"id": 7, "crop": "Cabbage", "market": "Jalpaiguri",
     "price": 1100, "demand": "Medium"},
    {"id": 8, "crop": "Cabbage", "market": "Medinipur",
     "price": 1250, "demand": "High"},
    {"id": 9, "crop": "Brinjal", "market": "Jalpaiguri",
     "price": 1900, "demand": "Medium"},
    {"id": 10, "crop": "Brinjal", "market": "Medinipur",
     "price": 2050, "demand": "High"},
    {"id": 11, "crop": "Cauliflower", "market": "Jalpaiguri",
     "price": 1750, "demand": "Medium"},
    {"id": 12, "crop": "Cauliflower", "market": "Medinipur",
     "price": 1680, "demand": "Medium"},
]

listings = [
    {
        "id": 1,
        "crop": "Potato",
        "quantity_quintals": 18,
        "location": "Jalpaiguri",
        "quality": "Grade A",
        "seller": "Demo Farmer Group",
        "status": "Available",
    },
    {
        "id": 2,
        "crop": "Tomato",
        "quantity_quintals": 7,
        "location": "Medinipur",
        "quality": "Grade A",
        "seller": "Demo FPO",
        "status": "Available",
    },
    {
        "id": 3,
        "crop": "Cabbage",
        "quantity_quintals": 12,
        "location": "Jalpaiguri",
        "quality": "Grade B",
        "seller": "Demo Farmer",
        "status": "Available",
    },
]


class ListingCreate(BaseModel):
    crop: str = Field(min_length=2, max_length=60)
    quantity_quintals: float = Field(gt=0, le=100000)
    location: str = Field(min_length=2, max_length=100)
    quality: str = Field(default="Not graded", max_length=40)
    seller: str = Field(min_length=2, max_length=100)


@app.get("/")
def root():
    return {
        "message": "Welcome to Kisaan Setu API",
        "docs": "/docs",
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/crops")
def get_crops(
    crop: Optional[str] = None,
    market: Optional[str] = None,
):
    result = crop_prices

    if crop:
        result = [
            item for item in result
            if item["crop"].lower() == crop.lower()
        ]

    if market:
        result = [
            item for item in result
            if item["market"].lower() == market.lower()
        ]

    return {
        "source_note": "Synthetic demo data, not live mandi prices.",
        "count": len(result),
        "items": result,
    }


@app.get("/api/markets")
def get_markets():
    return sorted({
        item["market"] for item in crop_prices
    })


@app.get("/api/compare")
def compare_crop(crop: str = Query(..., min_length=2)):
    items = [
        item for item in crop_prices
        if item["crop"].lower() == crop.lower()
    ]

    if not items:
        raise HTTPException(
            status_code=404,
            detail="No demo prices found for this crop.",
        )

    ordered = sorted(
        items,
        key=lambda item: item["price"],
        reverse=True,
    )

    return {
        "crop": crop.title(),
        "highest": ordered[0],
        "lowest": ordered[-1],
        "difference": (
            ordered[0]["price"] - ordered[-1]["price"]
        ),
        "items": ordered,
        "source_note": "Demo data only. Verify actual prices before selling.",
    }


@app.get("/api/listings")
def get_listings():
    return {
        "count": len(listings),
        "items": listings,
    }


@app.post("/api/listings", status_code=201)
def create_listing(payload: ListingCreate):
    new_listing = {
        "id": max(
            [item["id"] for item in listings],
            default=0,
        ) + 1,
        **payload.model_dump(),
        "status": "Available",
    }

    listings.append(new_listing)
    return new_listing
