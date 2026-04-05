import json
from pathlib import Path

from schemas.review_schema import RestaurantReviews
from src.baseline_extractor import aggregate_reviews, analyze_reviews_detailed


def main():
    file_path = Path("data/raw_reviews/sample_restaurant.json")

    with open(file_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    restaurant_data = RestaurantReviews(**raw_data)
    review_dicts = [review.model_dump() for review in restaurant_data.reviews]

    detailed_results = analyze_reviews_detailed(review_dicts)
    aggregated_scores = aggregate_reviews(review_dicts)

    print(f"\nRestaurant: {restaurant_data.restaurantName}")
    print(f"Overall Google Rating: {restaurant_data.overallRating}")

    print("\n" + "=" * 60)
    print("DETAILED REVIEW ANALYSIS")
    print("=" * 60)

    for item in detailed_results:
        print(f"\nReview ID: {item['reviewId']}")
        print(f"Text: {item['text']}")
        print("Detected Properties:")

        found_any = False
        for prop, signal in item["propertySignals"].items():
            if signal["mentioned"]:
                found_any = True
                print(
                    f"  - {prop}: polarity={signal['polarity']}, "
                    f"score={signal['score']}, "
                    f"matchedKeywords={signal['matchedKeywords']}"
                )

        if not found_any:
            print("  - No properties detected")

    print("\n" + "=" * 60)
    print("AGGREGATED RESTAURANT SCORES")
    print("=" * 60)

    for prop, info in aggregated_scores.items():
        print(
            f"{prop}: score={info['score']}, "
            f"supportCount={info['supportCount']}, "
            f"evidenceLabel={info['evidenceLabel']}"
        )


if __name__ == "__main__":
    main()