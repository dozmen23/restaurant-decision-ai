from src.llm_extractor import build_review_llm_prompt, parse_review_llm_output


def main():
    review_id = "mock_review_001"
    review_text = (
        "The staff were kind and attentive, the Bosphorus view was spectacular, "
        "and I would definitely stay again."
    )

    prompt = build_review_llm_prompt(review_id, review_text)
    print("=== Prompt ===")
    print(prompt)

    mock_response = {
        "reviewId": review_id,
        "detectedSignals": {
            "serviceQuality": {
                "detected": True,
                "sentiment": "positive",
                "strength": 0.8,
                "weight": 0.7,
                "evidenceText": "attentive",
            },
            "staffFriendliness": {
                "detected": True,
                "sentiment": "positive",
                "strength": 0.9,
                "weight": 0.8,
                "evidenceText": "staff were kind and attentive",
            },
            "foodQuality": {
                "detected": False,
                "sentiment": "neutral",
                "strength": 0.0,
                "weight": 0.0,
                "evidenceText": None,
            },
            "ambience": {
                "detected": False,
                "sentiment": "neutral",
                "strength": 0.0,
                "weight": 0.0,
                "evidenceText": None,
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
                "evidenceText": "would definitely stay again",
            },
            "viewQuality": {
                "detected": True,
                "sentiment": "positive",
                "strength": 0.95,
                "weight": 0.85,
                "evidenceText": "Bosphorus view was spectacular",
            },
        },
    }

    validated_output = parse_review_llm_output(mock_response)
    print("\n=== Validated Output ===")
    print(validated_output.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
