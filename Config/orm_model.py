from database import Base
from sqlalchemy import Column, Integer, String, Float

class Sales(Base): #(Base) -> indicates that this is not just a class but an ORM model (class=table)
    __tablename__ = "sales"

    index = Column(Integer, primary_key=True, index=True)
    Store_ID = Column(Integer)
    Date = Column(String)
    Dept = Column(Integer)
    Weekly_Sales = Column(String)
    IsHoliday = Column(Integer)
    Temperature = Column(Float)
    Fuel_Price = Column(Float)
    CPI = Column(Float)
    Unemployment = Column(Float)
    Type = Column(Float)
    Size = Column(Float)