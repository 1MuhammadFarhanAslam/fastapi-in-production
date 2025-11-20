from pydantic import BaseModel


class PredictionPayload(BaseModel):
    text: str