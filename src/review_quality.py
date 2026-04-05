def count_words(text: str) -> int:
    return len(text.strip().split())


def is_low_information(text: str) -> bool:
    low_info_phrases = {
        "good",
        "nice",
        "bad",
        "great",
        "ok",
        "okay",
        "normal",
        "güzel",
        "iyi",
        "eh",
        "idare eder"
    }

    return text.strip().lower() in low_info_phrases


def has_meaningful_text(text: str) -> bool:
    stripped = text.strip()
    return any(char.isalpha() for char in stripped)


def evaluate_review_quality(review: dict) -> dict:
    text = review.get("text", "").strip()

    if not text:
        return {
            "isUsable": False,
            "reason": "empty_text"
        }

    if not has_meaningful_text(text):
        return {
            "isUsable": False,
            "reason": "no_meaningful_text"
        }

    if count_words(text) < 3:
        return {
            "isUsable": False,
            "reason": "too_short"
        }

    if is_low_information(text):
        return {
            "isUsable": False,
            "reason": "low_information"
        }

    return {
        "isUsable": True,
        "reason": "accepted"
    }


def filter_usable_reviews(reviews: list[dict]) -> tuple[list[dict], list[dict]]:
    usable_reviews = []
    rejected_reviews = []

    for review in reviews:
        quality_result = evaluate_review_quality(review)

        enriched_review = {
            **review,
            "qualityCheck": quality_result
        }

        if quality_result["isUsable"]:
            usable_reviews.append(enriched_review)
        else:
            rejected_reviews.append(enriched_review)

    return usable_reviews, rejected_reviews