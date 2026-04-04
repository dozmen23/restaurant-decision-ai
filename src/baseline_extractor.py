from collections import defaultdict


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
        pos_hits = sum(1 for kw in keyword_groups["positive"] if kw in text_lower)
        neg_hits = sum(1 for kw in keyword_groups["negative"] if kw in text_lower)

        mentioned = (pos_hits + neg_hits) > 0

        if not mentioned:
            results[prop] = {
                "mentioned": False,
                "sentiment": None,
                "score": None
            }
            continue

        raw_score = pos_hits - neg_hits

        if raw_score > 0:
            sentiment = 0.85
        elif raw_score < 0:
            sentiment = 0.20
        else:
            sentiment = 0.50

        results[prop] = {
            "mentioned": True,
            "sentiment": sentiment,
            "score": int(sentiment * 100)
        }

    return results


def aggregate_reviews(reviews: list[dict]) -> dict:
    property_scores = defaultdict(list)

    for review in reviews:
        review_text = review["text"]
        analysis = analyze_review(review_text)

        for prop, result in analysis.items():
            if result["mentioned"] and result["sentiment"] is not None:
                property_scores[prop].append(result["sentiment"])

    final_output = {}

    for prop, sentiments in property_scores.items():
        avg_sentiment = sum(sentiments) / len(sentiments)
        final_output[prop] = {
            "score": round(avg_sentiment * 100, 2),
            "supportCount": len(sentiments),
            "evidenceLabel": (
                "strong" if len(sentiments) >= 3
                else "moderate" if len(sentiments) == 2
                else "weak"
            )
        }

    return final_output