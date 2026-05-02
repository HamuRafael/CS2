def serialize_comparison(comparison: dict) -> dict:
    return {
        "comparisonId": comparison.get("comparisonId"),
        "players": comparison.get("players"),
        "stats": comparison.get("stats", []),
        "summary": comparison.get("summary", []),
    }
