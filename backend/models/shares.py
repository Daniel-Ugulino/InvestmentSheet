from pydantic import BaseModel, Field, BeforeValidator
from typing import Optional, Annotated
from datetime import datetime, timezone
import math

PyObjectId = Annotated[str, BeforeValidator(str)]

class Shares(BaseModel):
    companyCode: str
    currentQuote: float
    max52Week: float
    min52Week: float
    dividendYield: float
    LPA: float
    VPA: float
    averageLiquidity: Optional[float] = None 
    market_options: Optional[float] = None 
    LTI: Optional[str] = '-'
    NLT: Optional[str] = '-'
    fairPrice: Optional[float] = None
    ceilingPrice: Optional[float] = None
    differenceToCeiling: Optional[float] = None
    shouldInvest: bool = Field(default=False)
    insertedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))    
    
    def __init__(self, **data):
        super().__init__(**data)
        self.fairPrice = round(self.__calc_fair_price(),2)
        self.ceilingPrice = round(self.__calc_ceiling_price(),2)
        self.differenceToCeiling = round(self.__dif_ceiling_price(),2)
        self.shouldInvest = self.__should_invest()
        
    def __calc_fair_price(self):
        return math.sqrt(22.5 * self.VPA * self.LPA)

    def __calc_ceiling_price(self):
        self.ceilingPrice = self.fairPrice * 0.8
        return self.ceilingPrice
    
    def __dif_ceiling_price(self):
        self.differenceToCeiling = (100 - (self.currentQuote * 100 / self.ceilingPrice)) / 100
        return self.differenceToCeiling
    
    def __should_invest(self):
        return self.dividendYield > 6 and self.currentQuote < self.ceilingPrice
    
    def __setattr__(self, name, value):
        return super().__setattr__(name, value)
