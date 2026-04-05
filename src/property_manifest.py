from config.properties import PROPERTY_DEFINITIONS, PROPERTY_ORDER


def build_property_manifest() -> dict:
    properties = []

    for key in PROPERTY_ORDER:
        definition = PROPERTY_DEFINITIONS[key]

        properties.append({
            "key": key,
            "displayName": definition["displayName"],
            "description": definition["description"]
        })

    return {
        "totalProperties": len(properties),
        "properties": properties
    }