from typing import Literal, Optional

from pydantic import BaseModel


LLMSentimentLabel = Literal["positive", "negative", "neutral", "mixed"]


class LLMPropertySignal(BaseModel):
    detected: bool
    sentiment: LLMSentimentLabel
    strength: float
    weight: float
    evidenceText: Optional[str] = None


class ReviewLLMDetectedSignals(BaseModel):
    serviceQuality: LLMPropertySignal
    staffFriendliness: LLMPropertySignal
    foodQuality: LLMPropertySignal
    ambience: LLMPropertySignal
    dateSuitability: LLMPropertySignal
    repeatVisitIntent: LLMPropertySignal
    viewQuality: LLMPropertySignal


class ReviewLLMExtractionOutput(BaseModel):
    reviewId: str
    detectedSignals: ReviewLLMDetectedSignals
