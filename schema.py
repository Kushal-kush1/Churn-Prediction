from pydantic import BaseModel

class CustomerData(BaseModel):
    CreditScore:float
    Geography:str
    Gender:str
    Age:int
    Tenure:int
    Balance:float
    NumOfProducts:int
    HasCrCard:int
    IsActiveMember:int
    EstimatedSalary:float
   
