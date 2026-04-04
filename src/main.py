import json
from pathlib import Path

from schemas.review_schema import RestaurantReviews
from src.baseline_extractor import aggregate_reviews


def main():
    file_path = Path("data/raw_reviews/sample_restaurant.json")

    with open(file_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    restaurant_data = RestaurantReviews(**raw_data)

    review_dicts = [review.model_dump() for review in restaurant_data.reviews]

    aggregated_scores = aggregate_reviews(review_dicts)

    print(f"\nRestaurant: {restaurant_data.restaurantName}")
    print(f"Overall Google Rating: {restaurant_data.overallRating}")
    print("\nReview-Based Property Scores:\n")

    for prop, info in aggregated_scores.items():
        print(
            f"{prop}: score={info['score']}, "
            f"supportCount={info['supportCount']}, "
            f"evidenceLabel={info['evidenceLabel']}"
        )


if __name__ == "__main__":
    main()