from pydantic import BaseModel
#from datetime import date

class SalesScheme(BaseModel):
    index: int
    Store_ID: int
    Date: str
    Dept: int
    Weekly_Sales: str
    IsHoliday: int
    Temperature: float
    Fuel_Price: float
    CPI: float
    Unemployment: float
    Type: float
    Size: float

    class Config:
        from_attributes = True #Pydantic knows it gets a ORM instance not just a plain dictionary