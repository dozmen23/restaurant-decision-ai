from schemas.llm_extraction_schema import LLMPropertySignal, ReviewLLMExtractionOutput


LLM_OVERRIDE_PROPERTIES = [
    "staffFriendliness",
    "foodQuality",
    "ambience",
    "repeatVisitIntent",
    "viewQuality",
]

LLM_POLARITY_TO_SCORE = {
    "positive": 85,
    "negative": 20,
    "neutral": 50,
    "mixed": 50,
}

LLM_POLARITY_TO_SENTIMENT = {
    "positive": 0.85,
    "negative": 0.20,
    "neutral": 0.50,
    "mixed": 0.50,
}


def map_llm_signal_to_baseline_signal(llm_signal: LLMPropertySignal) -> dict:
    matched_keywords = [llm_signal.evidenceText] if llm_signal.evidenceText else []

    return {
        "mentioned": True,
        "sentiment": LLM_POLARITY_TO_SENTIMENT[llm_signal.sentiment],
        "score": LLM_POLARITY_TO_SCORE[llm_signal.sentiment],
        "matchedKeywords": matched_keywords,
        "polarity": llm_signal.sentiment,
    }


def fuse_review_signals(
    baseline_signals: dict[str, dict],
    llm_output: ReviewLLMExtractionOutput,
) -> dict[str, dict]:
    fused_signals = {
        property_name: dict(signal)
        for property_name, signal in baseline_signals.items()
    }

    detected_signals = llm_output.detectedSignals.model_dump()

    for property_name in LLM_OVERRIDE_PROPERTIES:
        llm_signal = LLMPropertySignal(**detected_signals[property_name])

        if not llm_signal.detected:
            continue

        fused_signals[property_name] = map_llm_signal_to_baseline_signal(llm_signal)

    return fused_signals


def build_fusion_example() -> dict:
    baseline_signals = {
        "serviceQuality": {
            "mentioned": False,
            "sentiment": None,
            "score": None,
            "matchedKeywords": [],
            "polarity": None,
        },
        "staffFriendliness": {
            "mentioned": False,
            "sentiment": None,
            "score": None,
            "matchedKeywords": [],
            "polarity": None,
        },
        "foodQuality": {
            "mentioned": False,
            "sentiment": None,
            "score": None,
            "matchedKeywords": [],
            "polarity": None,
        },
        "ambience": {
            "mentioned": False,
            "sentiment": None,
            "score": None,
            "matchedKeywords": [],
            "polarity": None,
        },
        "dateSuitability": {
            "mentioned": False,
            "sentiment": None,
            "score": None,
            "matchedKeywords": [],
            "polarity": None,
        },
        "repeatVisitIntent": {
            "mentioned": False,
            "sentiment": None,
            "score": None,
            "matchedKeywords": [],
            "polarity": None,
        },
        "viewQuality": {
            "mentioned": False,
            "sentiment": None,
            "score": None,
            "matchedKeywords": [],
            "polarity": None,
        },
    }

    llm_output = ReviewLLMExtractionOutput(
        reviewId="mock_review_001",
        detectedSignals={
            "serviceQuality": {
                "detected": True,
                "sentiment": "positive",
                "strength": 0.8,
                "weight": 0.7,
                "evidenceText": "excellent service throughout the stay",
            },
            "staffFriendliness": {
                "detected": True,
                "sentiment": "positive",
                "strength": 0.9,
                "weight": 0.8,
                "evidenceText": "staff were kind and welcoming",
            },
            "foodQuality": {
                "detected": False,
                "sentiment": "neutral",
                "strength": 0.0,
                "weight": 0.0,
                "evidenceText": None,
            },
            "ambience": {
                "detected": True,
                "sentiment": "positive",
                "strength": 0.75,
                "weight": 0.6,
                "evidenceText": "beautiful atmosphere",
            },
            "dateSuitability": {
                "detected": False,
                "sentiment": "neutral",
                "strength": 0.0,
                "weight": 0.0,
                "evidenceText": None,
            },
            "repeatVisitIntent": {
                "detected": True,
                "sentiment": "positive",
                "strength": 0.85,
                "weight": 0.75,
                "evidenceText": "would stay again",
            },
            "viewQuality": {
                "detected": True,
                "sentiment": "positive",
                "strength": 0.95,
                "weight": 0.85,
                "evidenceText": "spectacular Bosphorus view",
            },
        },
    )

    return {
        "baselineSignals": baseline_signals,
        "llmOutput": llm_output.model_dump(),
        "fusedSignals": fuse_review_signals(baseline_signals, llm_output),
    }
