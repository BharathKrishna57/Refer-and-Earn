from sqlalchemy import Column, Integer, String, DateTime
from db.session import Base  # Make sure Base = declarative_base()
 
class PincodeMaster(Base):
    __tablename__ = "tbl_VHF_PINCODEMASTER"
 
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pincode = Column(String(6), index=True)
    cityName = Column(String(100))
    cityCode = Column(String(100))
    cityId = Column(Integer)
    stateCode = Column(String(100))
    stateName = Column(String(100))
    stateId = Column(Integer)
    countryCode = Column(String(100))
    countryName = Column(String(100))
    district = Column(String(100))
    tier = Column(Integer)
    isServiceable = Column(String(10))  # 'Yes' / 'No'
    createdAt = Column(DateTime)
    createdBy = Column(String(100))
    updatedAt = Column(DateTime)
    updatedBy = Column(String(100))
    place = Column(String(100))
