from pydantic import BaseModel
from typing import List


class Review(BaseModel):
    reviewId: str
    text: str
    publishTime: str


class RestaurantReviews(BaseModel):
    restaurantId: str
    restaurantName: str
    overallRating: float
    reviews: List[Review]