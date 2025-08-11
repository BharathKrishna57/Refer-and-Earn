from datetime import datetime
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.models.vfh_models import CustomerData, NewReferrerData
from app.db.session import get_db
from app.schemas.vfh_schemas import CustomerCheckRequest
from app.repository.refer_repository import ReferRepository
import requests
 
router = APIRouter()
 
# ---------- Check if Customer Exists ----------
# @router.post("/refer/check_or_create")
# def check_customer(payload: CustomerCheckRequest, db: Session = Depends(get_db)):
#     mobile = payload.mobilenumber
#     print("INPUT PAYLOAD",payload)
#     existing = db.query(CustomerData).filter(CustomerData.MOBILE_NUMBER == mobile).first()
#     lead_data = existing.__dict__
#     print("Existed lead",existing.__dict__)
#     print(lead_data)
#     print(lead_data["Customer_name"], lead_data["MOBILE_NUMBER"])
#     lead_input = {
#         "firstName": lead_data["Customer_name"],
#         "mobile": lead_data["MOBILE_NUMBER"],
#         }# ✅ correct
#     LEAD_CREATE_URL = "http://localhost:9000/api/v1/lead/enrollement"
#     response = requests.post(LEAD_CREATE_URL,json=lead_input)
#     print("LEADRESPONSE",response.json())
 
 
#     if existing:
#         return {
#             "status": "existing",
#             "customer": {
#                 "id": existing.customer_ID,
#                 "name": existing.Customer_name,
#                 "branch": existing.Branch,
#                 "dob": str(existing.DOB) if existing.DOB else None
#             }
#         }
 
#     return {"status": "new"}
 
# # ---------- Submit Referral ----------
# @router.post("/refer/submit_referral")
# def submit_referral(
#     customerMobile: str = Body(...),
#     customerName: str = Body(...),
#     customerPlace: str = Body(None),
#     referralName: str = Body(...),
#     referralMobile: str = Body(...),
#     referralPlace: str = Body(...),
#     db: Session = Depends(get_db)
# ):
#     repo = ReferRepository(db)
 
#     payload = {
#         "customerMobile": customerMobile,
#         "customerName": customerName,
#         "customerPlace": customerPlace,
#         "referralName": referralName,
#         "referralMobile": referralMobile,
#         "referralLocation": referralPlace
#     }
 
#     referral = repo.submit_referral(payload)
 
#     return {
#         "status": "referral_saved",
#         "referral": {
#             "reference_id": referral.EXISTING_CUSTID,
#             "name": referral.REFERAL_NAME,
#             "mobile": referral.REFERAL_MOBILE,
#             "created_date": str(referral.Created_Date)
#         }
#     }
 
 
@router.post("/refer/check_or_create")
def check_customer(payload: CustomerCheckRequest, db: Session = Depends(get_db)):
    mobile = payload.mobilenumber.strip()
 
    # Check in CustomerData
    existing = db.query(CustomerData).filter(CustomerData.MOBILE_NUMBER == mobile).first()
 
    if existing:
        print("Krishna@@@:", existing.__dict__)
        return {
            "status": "existing",
            "customer": {
                "id": existing.customer_ID,
                "name": existing.Customer_name,
                "branch": existing.Branch,
                "dob": str(existing.DOB) if existing.DOB else None
            }
        }
 
    # If not found in CustomerData, check in NewReferrerData
    referrer = db.query(NewReferrerData).filter(NewReferrerData.Mobile_Number == mobile).first()
    print("Bharath@@@@:", referrer)
    if referrer:
        print("Referrer found:", referrer.__dict__)
        return {
            "status": "existing",
            "customer": {
                "id": "NA",
                "name": referrer.Referrer_Name,
                "branch": "RT Nagar",
                "dob": None
            }
        }
 
    return {"status": "new"}
 
 
 
 
@router.post("/refer/submit_referral")
def submit_referral(
    customerMobile: str = Body(...),
    customerName: str = Body(...),
    customerPlace: str = Body(None),
    referralName: str = Body(...),
    referralMobile: str = Body(...),
    referralPlace: str = Body(...),
    db: Session = Depends(get_db)
):
    print("INPUT PAYLOAD", {
        "customerMobile": customerMobile,
        "customerName": customerName,
        "customerPlace": customerPlace,
        "referralName": referralName,
        "referralMobile": referralMobile,
        "referralPlace": referralPlace
    })
 
    # Saarathi expects one lead at a time – send customer lead
    # customer_payload = {
    #     "firstName": customerName,
    #     "mobile": customerMobile,
    #     "source": "refer-and-earn",
    #     "location": customerPlace
    # }
 
    referral_payload = {
        "firstName": referralName,
        "mobile": referralMobile,
        "source": "refer-and-earn",
        "location": referralPlace
    }
 
    REFERRAL_CREATE_URL = "http://localhost:9000/api/v1/lead/enrollement"
 
    # customer_response = requests.post(REFERRAL_CREATE_URL, json=customer_payload)
    referral_response = requests.post(REFERRAL_CREATE_URL, json=referral_payload)
 
    # print("CUSTOMER RESPONSE", customer_response.json())
    print("REFERRAL RESPONSE", referral_response.json())
 
    # Save referral into DB
    referral_input = {
        "customerName": customerName,
        "customerMobile": customerMobile,
        "customerPlace": customerPlace,
        "referralName": referralName,
        "referralMobile": referralMobile,
        "referralLocation": referralPlace
    }
 
    repo = ReferRepository(db)
    referral = repo.submit_referral(referral_input)
 
    return {
        "status": "referral_saved",
        # "customer_lead": customer_response.json(),
        "referral_lead": referral_response.json(),
        "referral": {
            "reference_id": referral.REFERENCE_ID,
            "name": referral.REFERAL_NAME,
            "mobile": referral.REFERAL_MOBILE,
            "created_date": str(referral.Created_Date)
        }
    }
 
 
 