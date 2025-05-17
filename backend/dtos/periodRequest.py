from pydantic import BaseModel
from datetime import date

class PeriodRequest(BaseModel):
    start_date: date
    end_date: date