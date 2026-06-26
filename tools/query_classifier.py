def needs_web_search(query):

    if not query:
        return False

    query = str(query).lower()

    keywords = [
        "latest",
        "today",
        "news",
        "weather",
        "temperature",
        "forecast",
        "current",
        "recent",
        "live",
        "score",
        "who won",
        "stock",
        "price",
        "search",
        "lookup",
        "internet",
        "update",
        "headline",
        "trending",
        "match",
        "result",
        "yesterday",
        "tomorrow"
    ]

    return any(
        keyword in query
        for keyword in keywords
    )