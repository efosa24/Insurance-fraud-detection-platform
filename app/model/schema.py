from pydantic import BaseModel

class FraudRequest(BaseModel):
    Month: str
    WeekOfMonth: int
    DayOfWeek: str
    Make: str
    AccidentArea: str
    Age: int
    Fault: str
    PolicyType: str
    VehicleCategory: str
    VehiclePrice: str
    Deductible: int
    DriverRating: int
    Year: int
    BasePolicy: str