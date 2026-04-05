from pydantic import BaseModel
from typing import Optional, Literal


EvidenceLabel = Literal["weak", "moderate", "strong"]


class QualityCheck(BaseModel):
    isUsable: bool
    reason: str


class PropertySignal(BaseModel):
    mentioned: bool
    sentiment: Optional[float] = None
    score: Optional[int] = None
    matchedKeywords: list[str]
    polarity: Optional[Literal["positive", "negative", "neutral"]] = None


class DetailedReviewAnalysisItem(BaseModel):
    reviewId: str
    text: str
    qualityCheck: QualityCheck
    propertySignals: dict[str, PropertySignal]


class RejectedReviewItem(BaseModel):
    reviewId: str
    text: str
    qualityCheck: QualityCheck


class PropertyEvidence(BaseModel):
    topMatchedKeywords: list[str]
    supportingReviewIds: list[str]
    supportingReviewSnippets: list[str]


class PropertyScore(BaseModel):
    score: float
    confidence: float
    supportCount: int
    evidenceLabel: EvidenceLabel
    evidence: PropertyEvidence


class ReviewSnapshot(BaseModel):
    totalReviewsFetched: int
    reviewsProcessed: int
    reviewsRejected: int
    lastReviewPublishTime: Optional[str] = None
    analysisVersion: str
    analyzedAt: str


class SummaryBlock(BaseModel):
    strengths: list[str]
    weaknesses: list[str]
    oneParagraphSummary: str


class DetailedAnalysisOutput(BaseModel):
    restaurantId: str
    restaurantName: str
    overallRating: float
    detailedReviewAnalysis: list[DetailedReviewAnalysisItem]
    rejectedReviews: list[RejectedReviewItem]


class RestaurantScoresOutput(BaseModel):
    restaurantId: str
    restaurantName: str
    overallRating: float
    reviewSnapshot: ReviewSnapshot
    reviewBasedScores: dict[str, PropertyScore]
    topReviewTags: list[str]
    summary: SummaryBlock