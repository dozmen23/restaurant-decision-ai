def adapt_place_to_pipeline_input(place: dict) -> dict:
    reviews = []

    for review in place.get("reviews", []):
        text_block = review.get("text")
        text = text_block.get("text") if isinstance(text_block, dict) else None

        if not text:
            continue

        reviews.append({
            "reviewId": review.get("name"),
            "text": text,
            "publishTime": review.get("publishTime"),
        })

    display_name = place.get("displayName")
    restaurant_name = (
        display_name.get("text")
        if isinstance(display_name, dict) and display_name.get("text")
        else place.get("name")
    )

    return {
        "restaurantId": place.get("id"),
        "restaurantName": restaurant_name,
        "overallRating": place.get("rating"),
        "reviews": reviews,
    }


def adapt_places_payload(payload: dict) -> list[dict]:
    return [
        adapt_place_to_pipeline_input(place)
        for place in payload.get("places", [])
    ]
