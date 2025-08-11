from sqlalchemy.orm import Session
from models.pincode import PincodeMaster


class PincodeRepository:
 
    def __init__(self, db: Session):
        self.db = db
 
    def get_by_pincode(self, pincode: str):
        """
        Fetch pincode details by exact 6-digit pincode.
        """
        return (
            self.db.query(PincodeMaster)
            .filter(PincodeMaster.pincode == pincode)
            .all()
        )
