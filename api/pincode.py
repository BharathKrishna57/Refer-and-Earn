from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
import httpx

from app.db.session import get_db
from app.models.pincode import PincodeMaster

router = APIRouter()


# -------------------------------
# GET /location -> Get places from India Post API
# -------------------------------
@router.get("/location")
async def get_location_by_pincode(
    pincode: str = Query(..., min_length=6, max_length=6)
):
    clean_pincode = pincode.strip()

    try:
        timeout = httpx.Timeout(10.0, connect=5.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(f"https://api.postalpincode.in/pincode/{clean_pincode}")
            response.raise_for_status()
            result = response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="India Post API returned an error")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Failed to reach India Post API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    if not result or result[0]["Status"] != "Success" or not result[0]["PostOffice"]:
        return {
            "message": "Pincode not found in external source",
            "data": {}
        }

    post_offices = result[0]["PostOffice"]

    # Extract shared fields from the first post office
    first_po = post_offices[0]

    response_data = {
        "countryName": first_po["Country"],
        "tier": 3,
        "district": first_po["District"],
        "pincode": clean_pincode,
        "cityName": first_po["Division"],
        "stateCode": first_po["State"][:2].upper(),
        "stateName": first_po["State"],
        "places": [po["Name"] for po in post_offices]
    }

    return {
        "message": "Fetched successfully",
        "data": response_data
    }


# -------------------------------
# POST /location/save -> Save selected place to DB
# -------------------------------
class PincodeSaveRequest(BaseModel):
    pincode: str
    place: str
    cityName: str
    district: str
    stateCode: str
    stateName: str
    countryName: str

@router.post("/location/save")
def save_selected_location(
    data: PincodeSaveRequest,
    db: Session = Depends(get_db)
):
    existing = db.query(PincodeMaster).filter(PincodeMaster.pincode == data.pincode).first()

    if existing:
        existing.place = data.place
        existing.cityName = data.cityName
        existing.district = data.district
        existing.stateCode = data.stateCode
        existing.stateName = data.stateName
        existing.countryCode = data.countryName[:3].upper()
        existing.countryName = data.countryName
        existing.tier = 3
        existing.isServiceable = "Yes"
        db.commit()
        db.refresh(existing)
        return {"message": "Updated", "id": existing.id}

    new_record = PincodeMaster(
        pincode=data.pincode,
        place=data.place,
        cityName=data.cityName,
        cityCode=None,
        cityId=None,
        district=data.district,
        stateCode=data.stateCode,
        stateName=data.stateName,
        stateId=None,
        countryCode=data.countryName[:3].upper(),
        countryName=data.countryName,
        tier=3,
        isServiceable="Yes",
        createdAt=datetime.now(),
        createdBy="system"
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return {"message": "Saved", "id": new_record.id}
