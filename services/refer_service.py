from sqlalchemy.orm import Session
from repository.refer_repository import ReferRepository

def handle_refer_request(db: Session, mobile: str, name: str = None):
    print("routerrepo")
    repo = ReferRepository(db)
    

    customer = repo.get_existing_customer(mobile)
    if customer:
        referral = repo.get_referral_data(mobile, name)
        print("referralemp:",referral)
            
            # referral_emp =repo.get_referral_data(mobile, name)
            # return {
            #     "status": "referral_found",
            #     "EXISTING_CUST_NAME": referral.EXISTING_CUST_NAME,
            #     "REFERAL_NAME": referral.REFERAL_NAME,
            #     "REFERAL_MOBILE": referral.REFERAL_MOBILE
            # }

        return {"status": "existing", "customer_name": customer.Customer_name}

    # referral = repo.get_referral_data(mobile, name)
    
    if not name:
        return {"error": "Customer name required for new entry"}

    new_customer = repo.create_customer(mobile, name)
    return {"status": "new_created", "customer_name": new_customer.Customer_name}
