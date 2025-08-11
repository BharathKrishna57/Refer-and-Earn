from sqlalchemy import Column, Integer, String, Date, Time, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
 
Base = declarative_base()
 
class CustomerData(Base):
    __tablename__ = "tbl_VFH_CUSTOMERDATA"
    Cust_INDEX = Column(Integer, primary_key=True, autoincrement=True)
    MOBILE_NUMBER = Column(String(10), nullable=False, unique=True)
    Customer_name = Column(String(200), nullable=False)
    DOB = Column(Date, nullable=True)  # not used now
    customer_ID = Column(String(100), nullable=False, unique=True)
    LOS_loan_number = Column(String(100), nullable=True)
    LMS_loan_Number = Column(String(100), nullable=True)
    Branch = Column(String(100), default="RT Nagar", nullable=False)
 
class ReferralData(Base):
    __tablename__ = "tbl_VFH_REFERALDATA"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    Created_Date = Column(Date, nullable=False)
    Created_Time = Column(Time, nullable=False)
    EXISTING_CUST_NAME = Column(String(100), nullable=False)
    EXISTING_CUST_MOBILE = Column(String(10), nullable=False)
    PushedToSaarathi = Column(Integer, default=0)
    EXISTING_CUSTID = Column(String(100), nullable=False)
    IS_EXISTING = Column(Integer, nullable=False)  # 0 = New, 1 = Existing
    REFERAL_NAME = Column(String(100), nullable=False)
    REFERAL_MOBILE = Column(String(10), nullable=False)
    REFERAL_PIN = Column(String(6), nullable=True)
    REFERAL_CITY = Column(String(100), nullable=True)
    REFERAL_LOCATION = Column(String(500), nullable=True)
    CUST_PLACE = Column(String(200), nullable=True)  # Added manually
    REFERENCE_ID = Column(String, unique=True)
   
   
class NewReferrerData(Base):
    __tablename__ = "tbl_VFH_NewReferrer"
 
    New_Ref_ID = Column(Integer, primary_key=True, autoincrement=True)
    Mobile_Number = Column(String(20), nullable=False, unique=True)
    Referrer_Name = Column(String(100))
    CreatedDate = Column(DateTime)
   
 
 