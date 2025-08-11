from pydantic import BaseModel
from typing import Optional

class CustomerCheckRequest(BaseModel):
    mobilenumber: str

class ReferralCreate(BaseModel):
    customerMobile: str
    customerName: str
    customerPlace: Optional[str] = None
    referralName: str
    referralMobile: str
    referralLocation: str

class ReferralResponse(BaseModel):
    referral: dict
