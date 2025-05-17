from pydantic import BaseModel, Field, BeforeValidator
from typing import Optional, Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]

class Company(BaseModel):
    name: str
    code: str
    fitch_url: Optional[str] = None
