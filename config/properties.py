PROPERTY_DEFINITIONS = {
    "foodQuality": {
        "displayName": "Food Quality",
        "description": "Taste, flavor, and overall food satisfaction.",
        "positive": ["amazing food", "great food", "delicious", "tasty", "lezzetli", "harika yemek"],
        "negative": ["bad food", "cold food", "bland", "tasteless", "kötü yemek"]
    },
    "staffFriendliness": {
        "displayName": "Staff Friendliness",
        "description": "Friendliness, politeness, and helpfulness of staff.",
        "positive": ["friendly staff", "polite", "kind", "helpful", "güler yüzlü", "nazik"],
        "negative": ["rude", "unfriendly", "kaba", "ilgisiz"]
    },
    "ambience": {
        "displayName": "Ambience",
        "description": "Atmosphere, mood, decor, and overall environment.",
        "positive": ["atmosphere", "ambiance", "ambience", "lovely", "cozy", "romantic", "atmosfer"],
        "negative": ["boring", "noisy", "dark", "rahatsız"]
    },
    "speed": {
        "displayName": "Speed",
        "description": "Service speed and waiting time.",
        "positive": ["fast service", "quick", "hızlı"],
        "negative": ["slow", "late", "waited too long", "geç geldi", "yavaş"]
    },
    "viewQuality": {
        "displayName": "View Quality",
        "description": "Quality of the view, scenery, or special visual setting.",
        "positive": ["great view", "beautiful view", "bosphorus view", "manzara"],
        "negative": ["no view", "bad view"]
    },
    "dateSuitability": {
        "displayName": "Date Suitability",
        "description": "Suitability for romantic dinners or special dates.",
        "positive": ["romantic", "nice for a date", "date night", "special dinner"],
        "negative": ["not good for a date"]
    },
    "cleanliness": {
        "displayName": "Cleanliness",
        "description": "Cleanliness and hygiene of the place.",
        "positive": ["clean", "spotless", "hijyenik", "temiz"],
        "negative": ["dirty", "filthy", "kirli"]
    },
    "groupSuitability": {
        "displayName": "Group Suitability",
        "description": "Suitability for families or groups of friends.",
        "positive": ["good for groups", "family dinner", "great for friends", "group dinner"],
        "negative": ["too small for groups", "not good for groups"]
    }
}


PROPERTY_ORDER = list(PROPERTY_DEFINITIONS.keys())