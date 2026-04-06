from pydantic import BaseModel
from pydantic import BaseModel, Field

class CodeRequest(BaseModel):
    code: str = Field(..., min_length=1)
