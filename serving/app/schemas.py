
from pydantic import BaseModel

class Input(BaseModel):
    features: list[float]
