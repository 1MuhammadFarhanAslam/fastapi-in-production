from pydantic import BaseModel
from typing import Dict, Any


class TextPredictionResponse(BaseModel):
    prediction: Dict[str, Any]