import json
from pathlib import Path
from datetime import datetime, timezone

from schemas.review_schema import RestaurantReviews
from schemas.output_schema import (
    DetailedAnalysisOutput,
    MetaMetricsBlock,
    RestaurantScoresOutput,
    ReviewSnapshot,
    SummaryBlock,
)
from src.baseline_extractor import (
    analyze_reviews_detailed,
    aggregate_reviews,
    build_meta_metrics,
)
from src.adapters.google_places_adapter import adapt_places_payload
from src.property_manifest import build_property_manifest
from src.review_quality import filter_usable_reviews


def build_pipeline_outputs(restaurant_data: RestaurantReviews) -> tuple[DetailedAnalysisOutput, RestaurantScoresOutput, dict]:
    review_dicts = [review.model_dump() for review in restaurant_data.reviews]
    usable_reviews, rejected_reviews = filter_usable_reviews(review_dicts)

    detailed_results = analyze_reviews_detailed(usable_reviews)
    aggregated_bundle = aggregate_reviews(usable_reviews)
    meta_metrics = build_meta_metrics(
        aggregated_bundle["reviewBasedScores"],
        restaurant_data.overallRating,
    )

    review_times = [review.publishTime for review in restaurant_data.reviews]
    last_review_time = max(review_times) if review_times else None

    detailed_payload = DetailedAnalysisOutput(
        restaurantId=restaurant_data.restaurantId,
        restaurantName=restaurant_data.restaurantName,
        overallRating=restaurant_data.overallRating,
        detailedReviewAnalysis=detailed_results,
        rejectedReviews=[
            {
                "reviewId": review["reviewId"],
                "text": review["text"],
                "qualityCheck": review["qualityCheck"]
            }
            for review in rejected_reviews
        ]
    )

    scores_payload = RestaurantScoresOutput(
        restaurantId=restaurant_data.restaurantId,
        restaurantName=restaurant_data.restaurantName,
        overallRating=restaurant_data.overallRating,
        reviewSnapshot=ReviewSnapshot(
            totalReviewsFetched=len(restaurant_data.reviews),
            reviewsProcessed=len(usable_reviews),
            reviewsRejected=len(rejected_reviews),
            lastReviewPublishTime=last_review_time,
            analysisVersion="baseline-keyword-v2-quality-filter",
            analyzedAt=datetime.now(timezone.utc).isoformat()
        ),
        reviewBasedScores=aggregated_bundle["reviewBasedScores"],
        metaMetrics=MetaMetricsBlock(**meta_metrics),
        topReviewTags=aggregated_bundle["topReviewTags"],
        summary=SummaryBlock(**aggregated_bundle["summary"])
    )

    run_context = {
        "adaptedReviewCount": len(restaurant_data.reviews),
        "usableReviewCount": len(usable_reviews),
    }

    return detailed_payload, scores_payload, run_context


def main():
    input_path = Path("data/raw_reviews/sample_restaurant.json")
    google_places_input_path = Path("data/raw_reviews/google_places_payload.json")
    detailed_output_path = Path("data/processed_reviews/detailed_analysis.json")
    scores_output_path = Path("data/processed_reviews/restaurant_scores.json")
    manifest_output_path = Path("data/processed_reviews/property_manifest.json")
    property_manifest = build_property_manifest()

    if google_places_input_path.exists():
        input_path = google_places_input_path
        with open(input_path, "r", encoding="utf-8") as f:
            raw_payload = json.load(f)

        adapted_places = adapt_places_payload(raw_payload)
        if not adapted_places:
            raise ValueError("Google Places payload did not produce any adapted places.")
        selected_place = adapted_places[0]
        restaurant_data = RestaurantReviews(**selected_place)
        detailed_payload, scores_payload, run_context = build_pipeline_outputs(
            restaurant_data
        )
        selected_place_name = restaurant_data.restaurantName
    else:
        with open(input_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        restaurant_data = RestaurantReviews(**raw_data)
        detailed_payload, scores_payload, run_context = build_pipeline_outputs(
            restaurant_data
        )
        selected_place_name = restaurant_data.restaurantName

    detailed_output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(detailed_output_path, "w", encoding="utf-8") as f:
        json.dump(detailed_payload.model_dump(), f, ensure_ascii=False, indent=2)

    with open(scores_output_path, "w", encoding="utf-8") as f:
        json.dump(scores_payload.model_dump(), f, ensure_ascii=False, indent=2)

    with open(manifest_output_path, "w", encoding="utf-8") as f:
        json.dump(property_manifest, f, ensure_ascii=False, indent=2)

    print(f"\nDetailed analysis saved to: {detailed_output_path}")
    print(f"Restaurant scores saved to: {scores_output_path}")
    print(f"Property manifest saved to: {manifest_output_path}")
    print(f"Loaded file: {input_path}")
    print(f"Selected place: {selected_place_name}")
    print(f"Adapted reviews: {run_context['adaptedReviewCount']}")
    print(f"Usable reviews: {run_context['usableReviewCount']}")


if __name__ == "__main__":
    main()
