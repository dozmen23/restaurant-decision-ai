from collections import defaultdict, Counter


PROPERTY_KEYWORDS = {
    "foodQuality": {
        "positive": ["amazing food", "great food", "delicious", "tasty", "lezzetli", "harika yemek"],
        "negative": ["bad food", "cold food", "bland", "tasteless", "kötü yemek"]
    },
    "staffFriendliness": {
        "positive": ["friendly staff", "polite", "kind", "helpful", "güler yüzlü", "nazik"],
        "negative": ["rude", "unfriendly", "kaba", "ilgisiz"]
    },
    "ambience": {
        "positive": ["atmosphere", "ambiance", "ambience", "lovely", "cozy", "romantic", "atmosfer"],
        "negative": ["boring", "noisy", "dark", "rahatsız"]
    },
    "speed": {
        "positive": ["fast service", "quick", "hızlı"],
        "negative": ["slow", "late", "waited too long", "geç geldi", "yavaş"]
    },
    "viewQuality": {
        "positive": ["great view", "beautiful view", "bosphorus view", "manzara"],
        "negative": ["no view", "bad view"]
    },
    "dateSuitability": {
        "positive": ["romantic", "nice for a date", "date night", "special dinner"],
        "negative": ["not good for a date"]
    },
    "cleanliness": {
        "positive": ["clean", "spotless", "hijyenik", "temiz"],
        "negative": ["dirty", "filthy", "kirli"]
    }
}


def analyze_review(text: str) -> dict:
    text_lower = text.lower()
    results = {}

    for prop, keyword_groups in PROPERTY_KEYWORDS.items():
        positive_matches = [kw for kw in keyword_groups["positive"] if kw in text_lower]
        negative_matches = [kw for kw in keyword_groups["negative"] if kw in text_lower]

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


def analyze_reviews_detailed(reviews: list[dict]) -> list[dict]:
    detailed_results = []

    for review in reviews:
        analysis = analyze_review(review["text"])
        detailed_results.append({
            "reviewId": review["reviewId"],
            "text": review["text"],
            "propertySignals": analysis
        })

    return detailed_results


def aggregate_reviews(reviews: list[dict]) -> dict:
    property_scores = defaultdict(list)
    property_polarities = defaultdict(list)
    keyword_counter = Counter()

    for review in reviews:
        review_text = review["text"]
        analysis = analyze_review(review_text)

        for prop, result in analysis.items():
            if result["mentioned"] and result["sentiment"] is not None:
                property_scores[prop].append(result["sentiment"])
                property_polarities[prop].append(result["polarity"])
                keyword_counter.update(result["matchedKeywords"])

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
            )
        }

    top_review_tags = [tag for tag, _ in keyword_counter.most_common(5)]

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
            "strengths": strengths,
            "weaknesses": weaknesses,
            "oneParagraphSummary": summary_text
        }
    }


def build_summary(final_scores: dict, strengths: list[str], weaknesses: list[str]) -> str:
    if not final_scores:
        return "Not enough review evidence to generate a meaningful summary."

    strong_part = (
        f"Strongest signals are {', '.join(strengths)}."
        if strengths else
        "No clearly dominant strengths were detected."
    )

    weak_part = (
        f"Weaker signals are {', '.join(weaknesses)}."
        if weaknesses else
        "No major weaknesses were detected from the current reviews."
    )

    return f"Review analysis suggests that this restaurant stands out mainly through the following aspects. {strong_part} {weak_part}"