import json
from pathlib import Path
from datetime import datetime, timezone

from schemas.review_schema import RestaurantReviews
from src.baseline_extractor import analyze_reviews_detailed, aggregate_reviews


def main():
    input_path = Path("data/raw_reviews/sample_restaurant.json")
    detailed_output_path = Path("data/processed_reviews/detailed_analysis.json")
    scores_output_path = Path("data/processed_reviews/restaurant_scores.json")

    with open(input_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    restaurant_data = RestaurantReviews(**raw_data)
    review_dicts = [review.model_dump() for review in restaurant_data.reviews]

    detailed_results = analyze_reviews_detailed(review_dicts)
    aggregated_bundle = aggregate_reviews(review_dicts)

    review_times = [review.publishTime for review in restaurant_data.reviews]
    last_review_time = max(review_times) if review_times else None

    detailed_payload = {
        "restaurantId": restaurant_data.restaurantId,
        "restaurantName": restaurant_data.restaurantName,
        "overallRating": restaurant_data.overallRating,
        "detailedReviewAnalysis": detailed_results
    }

    scores_payload = {
        "restaurantId": restaurant_data.restaurantId,
        "restaurantName": restaurant_data.restaurantName,
        "overallRating": restaurant_data.overallRating,
        "reviewSnapshot": {
            "totalReviewsFetched": len(restaurant_data.reviews),
            "reviewsProcessed": len(review_dicts),
            "lastReviewPublishTime": last_review_time,
            "analysisVersion": "baseline-keyword-v1",
            "analyzedAt": datetime.now(timezone.utc).isoformat()
        },
        "reviewBasedScores": aggregated_bundle["reviewBasedScores"],
        "topReviewTags": aggregated_bundle["topReviewTags"],
        "summary": aggregated_bundle["summary"]
    }

    detailed_output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(detailed_output_path, "w", encoding="utf-8") as f:
        json.dump(detailed_payload, f, ensure_ascii=False, indent=2)

    with open(scores_output_path, "w", encoding="utf-8") as f:
        json.dump(scores_payload, f, ensure_ascii=False, indent=2)

    print(f"\nDetailed analysis saved to: {detailed_output_path}")
    print(f"Restaurant scores saved to: {scores_output_path}")


if __name__ == "__main__":
    main()