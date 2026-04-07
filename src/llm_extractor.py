import json
import os
from urllib import error, request

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


def build_review_llm_json_schema() -> dict:
    property_signal_schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "detected": {"type": "boolean"},
            "sentiment": {
                "type": "string",
                "enum": ["positive", "negative", "neutral", "mixed"],
            },
            "strength": {"type": "number", "minimum": 0.0, "maximum": 1.0},
            "weight": {"type": "number", "minimum": 0.0, "maximum": 1.0},
            "evidenceText": {"type": ["string", "null"]},
        },
        "required": [
            "detected",
            "sentiment",
            "strength",
            "weight",
            "evidenceText",
        ],
    }

    return {
        "name": "review_llm_extraction_output",
        "strict": True,
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "reviewId": {"type": "string"},
                "detectedSignals": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        property_name: property_signal_schema
                        for property_name in LLM_PROPERTIES
                    },
                    "required": LLM_PROPERTIES,
                },
            },
            "required": ["reviewId", "detectedSignals"],
        },
    }


def build_review_llm_prompt(review_id: str, review_text: str) -> str:
    return (
        "You are extracting structured restaurant review signals.\n"
        "Return JSON only. Do not add markdown, comments, or explanation.\n"
        "The JSON must match the ReviewLLMExtractionOutput schema exactly.\n"
        "Only evaluate these properties: "
        "serviceQuality, staffFriendliness, foodQuality, ambience, "
        "dateSuitability, repeatVisitIntent, viewQuality.\n"
        "For each property return:\n"
        "- detected: boolean\n"
        "- sentiment: one of positive, negative, neutral, mixed\n"
        "- strength: float between 0.0 and 1.0\n"
        "- weight: float between 0.0 and 1.0\n"
        "- evidenceText: string or null\n\n"
        "If detected is false, sentiment must be neutral, strength must be 0.0, "
        "weight must be 0.0, and evidenceText must be null.\n\n"
        f"reviewId: {review_id}\n"
        "reviewText:\n"
        f"{review_text}"
    )


def parse_review_llm_output(raw_output: dict) -> ReviewLLMExtractionOutput:
    return ReviewLLMExtractionOutput(**raw_output)


def run_llm_extraction_for_review(
    review_id: str,
    review_text: str,
) -> ReviewLLMExtractionOutput:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required to run LLM extraction.")

    prompt = build_review_llm_prompt(review_id, review_text)
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You extract structured restaurant review signals and return "
                    "schema-valid JSON only."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": build_review_llm_json_schema(),
        },
    }

    http_request = request.Request(
        url="https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(http_request) as response:
            response_payload = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"OpenAI API request failed with status {exc.code}: {error_body}"
        ) from exc
    except error.URLError as exc:
        raise RuntimeError(f"OpenAI API request failed: {exc.reason}") from exc

    try:
        message = response_payload["choices"][0]["message"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(
            "OpenAI API response is missing expected message fields."
        ) from exc

    if message.get("refusal"):
        raise RuntimeError(f"OpenAI model refused the request: {message['refusal']}")

    content = message.get("content")
    if isinstance(content, str):
        json_content = content
    elif isinstance(content, list):
        try:
            json_content = content[0]["text"]
        except (IndexError, KeyError, TypeError) as exc:
            raise RuntimeError(
                "OpenAI API response content list did not contain text."
            ) from exc
    else:
        raise RuntimeError("OpenAI API response did not contain JSON content.")

    try:
        parsed_output = json.loads(json_content)
    except json.JSONDecodeError as exc:
        raise RuntimeError("OpenAI API response returned invalid JSON.") from exc

    try:
        return parse_review_llm_output(parsed_output)
    except Exception as exc:
        raise RuntimeError("OpenAI API response failed schema validation.") from exc
