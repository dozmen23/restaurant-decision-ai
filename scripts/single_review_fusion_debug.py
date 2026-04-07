import json
from pathlib import Path

from src.adapters.google_places_adapter import adapt_places_payload
from src.baseline_extractor import analyze_review
from src.llm_extractor import run_llm_extraction_for_review
from src.review_fusion import fuse_review_signals


def load_single_real_review() -> tuple[str, str]:
    input_path = Path("data/raw_reviews/google_places_payload.json")

    with open(input_path, "r", encoding="utf-8") as f:
        raw_payload = json.load(f)

    adapted_places = adapt_places_payload(raw_payload)
    if not adapted_places:
        raise ValueError("Google Places payload did not produce any adapted places.")

    selected_place = adapted_places[0]
    if not selected_place["reviews"]:
        raise ValueError("Selected place does not contain any adapted reviews.")

    selected_review = selected_place["reviews"][0]
    return selected_review["reviewId"], selected_review["text"]


def main():
    review_id, review_text = load_single_real_review()

    baseline_signals = analyze_review(review_text)
    llm_output = run_llm_extraction_for_review(review_id, review_text)
    fused_signals = fuse_review_signals(baseline_signals, llm_output)

    print("=== Review ID ===")
    print(review_id)

    print("\n=== Review Text ===")
    print(review_text)

    print("\n=== Baseline Signals ===")
    print(json.dumps(baseline_signals, ensure_ascii=False, indent=2))

    print("\n=== LLM Output ===")
    print(llm_output.model_dump_json(indent=2))

    print("\n=== Fused Signals ===")
    print(json.dumps(fused_signals, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
