import json

from schemas.llm_extraction_schema import ReviewLLMExtractionOutput


LLM_PROPERTIES = [
    "serviceQuality",
    "staffFriendliness",
    "foodQuality",
    "ambience",
    "dateSuitability",
    "repeatVisitIntent",
    "viewQuality",
]


def build_review_llm_prompt(review_id: str, review_text: str) -> str:
    response_template = {
        "reviewId": review_id,
        "detectedSignals": {
            property_name: {
                "detected": False,
                "sentiment": "neutral",
                "strength": 0.0,
                "weight": 0.0,
                "evidenceText": None,
            }
            for property_name in LLM_PROPERTIES
        },
    }

    return (
        "You are extracting structured restaurant review signals.\n"
        "Return JSON only. Do not add markdown, comments, or explanation.\n"
        "The JSON must match the ReviewLLMExtractionOutput schema exactly.\n"
        "Only evaluate these properties:\n"
        "- serviceQuality\n"
        "- staffFriendliness\n"
        "- foodQuality\n"
        "- ambience\n"
        "- dateSuitability\n"
        "- repeatVisitIntent\n"
        "- viewQuality\n\n"
        "For each property return:\n"
        "- detected: boolean\n"
        "- sentiment: one of positive, negative, neutral, mixed\n"
        "- strength: float\n"
        "- weight: float\n"
        "- evidenceText: string or null\n\n"
        "Review ID:\n"
        f"{review_id}\n\n"
        "Review Text:\n"
        f"{review_text}\n\n"
        "Expected JSON shape:\n"
        f"{json.dumps(response_template, ensure_ascii=False, indent=2)}"
    )


def parse_review_llm_output(raw_output: dict) -> ReviewLLMExtractionOutput:
    return ReviewLLMExtractionOutput(**raw_output)
