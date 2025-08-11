from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from models.vfh_models import CustomerData, ReferralData, NewReferrerData


class ReferRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_existing_customer(self, mobile: str):
        return self.db.query(CustomerData)\
            .filter(
                CustomerData.MOBILE_NUMBER == mobile,
                CustomerData.Customer_name.isnot(None),
                CustomerData.Customer_name != ''
            ).first()

    def get_existing_referrer(self, mobile: str):
        return self.db.query(NewReferrerData)\
            .filter(NewReferrerData.Mobile_Number == mobile).first()

    def get_existing_cust_id_from_referral(self, mobile: str):
        referral_record = self.db.query(ReferralData)\
            .filter(ReferralData.EXISTING_CUST_MOBILE == mobile)\
            .order_by(ReferralData.ID.desc())\
            .first()
        return referral_record.EXISTING_CUSTID if referral_record else None

    def generate_reference_id(self):
        latest_id = self.db.query(func.max(ReferralData.ID)).scalar() or 0
        return f"RF{1000000000 + latest_id + 1}"

    def generate_customer_id_from_referral_table(self):
        """Generate CU ID from ReferralData only, excluding IDs already present in CustomerData."""

        # Step 1: Get all CU IDs from CustomerData
        customerdata_ids = set(
            row.customer_ID
            for row in self.db.query(CustomerData.customer_ID)
            .filter(CustomerData.customer_ID.like("CU%"))
            .all()
            if row.customer_ID
        )

        # Step 2: Get latest CU ID from ReferralData not in CustomerData
        referral_records = (
            self.db.query(ReferralData)
            .filter(ReferralData.EXISTING_CUSTID.like("CU%"))
            .order_by(ReferralData.ID.desc())
            .all()
        )

        for record in referral_records:
            cust_id = record.EXISTING_CUSTID
            if cust_id and cust_id not in customerdata_ids:
                try:
                    last_num = int(cust_id[2:])
                    return f"CU{last_num + 1:06d}"
                except Exception as e:
                    print("Error parsing EXISTING_CUSTID:", e)
                    break

        # Fallback if no CU IDs found
        return "CU12525"

    def submit_referral(self, payload: dict):
        now = datetime.now()

        mobile = payload["customerMobile"]
        name = payload["customerName"]
        place = payload.get("customerPlace")
        referral_name = payload["referralName"]
        referral_mobile = payload["referralMobile"]
        referral_location = payload["referralLocation"]

        customer_id = None
        is_existing = 0

        # Step 1: Check if customer exists in CustomerData
        existing_customer = self.get_existing_customer(mobile)
        if existing_customer and existing_customer.customer_ID:
            customer_id = existing_customer.customer_ID
            is_existing = 1

        else:
            # Step 2: Check if referred before
            existing_referral_id = self.get_existing_cust_id_from_referral(mobile)
            if existing_referral_id:
                customer_id = existing_referral_id
                is_existing = 1
            else:
                # Step 3: Generate new customer ID
                customer_id = self.generate_customer_id_from_referral_table()
                is_existing = 0

                # Add to NewReferrerData
                new_ref = NewReferrerData(
                    Mobile_Number=mobile,
                    Referrer_Name=name,
                    CreatedDate=now
                )
                self.db.add(new_ref)

        # Step 4: Generate Reference ID
        reference_id = self.generate_reference_id()

        # Step 5: Create ReferralData entry
        referral = ReferralData(
            Created_Date=now.date(),
            Created_Time=now.time(),
            EXISTING_CUST_NAME=name,
            EXISTING_CUST_MOBILE=mobile,
            EXISTING_CUSTID=customer_id,
            IS_EXISTING=is_existing,
            REFERAL_NAME=referral_name,
            REFERAL_MOBILE=referral_mobile,
            REFERAL_LOCATION=referral_location,
            CUST_PLACE=place if not is_existing else None,
            PushedToSaarathi=0,
            REFERENCE_ID=reference_id
        )

        self.db.add(referral)
        self.db.commit()
        self.db.refresh(referral)

        return referral
