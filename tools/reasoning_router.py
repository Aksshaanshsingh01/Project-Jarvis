def needs_deep_reasoning(query):

    if not query:
        return False

    query = query.lower()

    reasoning_keywords = [

        "plan",
        "strategy",
        "roadmap",
        "compare",
        "comparison",
        "analyze",
        "analysis",
        "pros and cons",
        "which is better",
        "recommend",
        "evaluate",
        "career",
        "step by step",
        "design",
        "architecture",
        "implement",
        "build",
        "debug",
        "why",
        "how would",
        "future",
        "tradeoff",
        "research",
        "optimize",
        "explain deeply"

    ]

    return any(
        keyword in query
        for keyword in reasoning_keywords
    )