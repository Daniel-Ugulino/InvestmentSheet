from pydantic import BaseModel, Field, BeforeValidator
from typing import Optional, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class Company(BaseModel):
    name: str
    code: str
    fitch_url: Optional[str] = None
    
    def to_dump(self):
        return self.model_dump(by_alias=True)
