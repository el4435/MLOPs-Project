from pydantic import BaseModel

class Input(BaseModel):
    features: list  # e.g., [hour, location, other_feat1, other_feat2]
