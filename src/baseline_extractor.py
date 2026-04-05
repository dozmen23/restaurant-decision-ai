from collections import defaultdict, Counter
from config.properties import PROPERTY_DEFINITIONS


def get_display_name(property_key: str) -> str:
    return PROPERTY_DEFINITIONS.get(property_key, {}).get("displayName", property_key)


def make_snippet(text: str, max_len: int = 120) -> str:
    text = text.strip()
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def analyze_review(text: str) -> dict:
    text_lower = text.lower()
    results = {}

    for prop, definition in PROPERTY_DEFINITIONS.items():
        positive_matches = [kw for kw in definition["positive"] if kw in text_lower]
        negative_matches = [kw for kw in definition["negative"] if kw in text_lower]

        pos_hits = len(positive_matches)
        neg_hits = len(negative_matches)

        mentioned = (pos_hits + neg_hits) > 0

        if not mentioned:
            results[prop] = {
                "mentioned": False,
                "sentiment": None,
                "score": None,
                "matchedKeywords": [],
                "polarity": None
            }
            continue

        raw_score = pos_hits - neg_hits

        if raw_score > 0:
            sentiment = 0.85
            polarity = "positive"
        elif raw_score < 0:
            sentiment = 0.20
            polarity = "negative"
        else:
            sentiment = 0.50
            polarity = "neutral"

        results[prop] = {
            "mentioned": True,
            "sentiment": sentiment,
            "score": int(sentiment * 100),
            "matchedKeywords": positive_matches + negative_matches,
            "polarity": polarity
        }

    return results


def analyze_reviews_detailed(usable_reviews: list[dict]) -> list[dict]:
    detailed_results = []

    for review in usable_reviews:
        analysis = analyze_review(review["text"])
        detailed_results.append({
            "reviewId": review["reviewId"],
            "text": review["text"],
            "qualityCheck": review["qualityCheck"],
            "propertySignals": analysis
        })

    return detailed_results


def aggregate_reviews(usable_reviews: list[dict]) -> dict:
    property_scores = defaultdict(list)
    property_keywords = defaultdict(Counter)
    property_review_ids = defaultdict(list)
    property_review_snippets = defaultdict(list)
    global_keyword_counter = Counter()

    for review in usable_reviews:
        review_id = review["reviewId"]
        review_text = review["text"]
        review_snippet = make_snippet(review_text)

        analysis = analyze_review(review_text)

        for prop, result in analysis.items():
            if result["mentioned"] and result["sentiment"] is not None:
                property_scores[prop].append(result["sentiment"])
                property_review_ids[prop].append(review_id)
                property_review_snippets[prop].append(review_snippet)
                property_keywords[prop].update(result["matchedKeywords"])
                global_keyword_counter.update(result["matchedKeywords"])

    final_scores = {}

    for prop, sentiments in property_scores.items():
        avg_sentiment = sum(sentiments) / len(sentiments)
        support_count = len(sentiments)
        confidence = min(1.0, 0.5 + (support_count * 0.1))

        final_scores[prop] = {
            "score": round(avg_sentiment * 100, 2),
            "confidence": round(confidence, 2),
            "supportCount": support_count,
            "evidenceLabel": (
                "strong" if support_count >= 3
                else "moderate" if support_count == 2
                else "weak"
            ),
            "evidence": {
                "topMatchedKeywords": [
                    keyword for keyword, _ in property_keywords[prop].most_common(3)
                ],
                "supportingReviewIds": property_review_ids[prop][:3],
                "supportingReviewSnippets": property_review_snippets[prop][:3]
            }
        }

    top_review_tags = [tag for tag, _ in global_keyword_counter.most_common(5)]

    strengths = []
    weaknesses = []

    for prop, info in final_scores.items():
        if info["score"] >= 80:
            strengths.append(prop)
        elif info["score"] <= 40:
            weaknesses.append(prop)

    summary_text = build_summary(final_scores, strengths, weaknesses)

    return {
        "reviewBasedScores": final_scores,
        "topReviewTags": top_review_tags,
        "summary": {
            "strengths": [get_display_name(p) for p in strengths],
            "weaknesses": [get_display_name(p) for p in weaknesses],
            "oneParagraphSummary": summary_text
        }
    }


def build_summary(final_scores: dict, strengths: list[str], weaknesses: list[str]) -> str:
    if not final_scores:
        return "Not enough review evidence to generate a meaningful summary."

    strength_names = [get_display_name(p) for p in strengths]
    weakness_names = [get_display_name(p) for p in weaknesses]

    strong_part = (
        f"Strongest signals are {', '.join(strength_names)}."
        if strength_names else
        "No clearly dominant strengths were detected."
    )

    weak_part = (
        f"Weaker signals are {', '.join(weakness_names)}."
        if weakness_names else
        "No major weaknesses were detected from the current reviews."
    )

    return (
        "Review analysis suggests that this restaurant stands out mainly through "
        f"the following aspects. {strong_part} {weak_part}"
    )