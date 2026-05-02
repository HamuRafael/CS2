from collections import defaultdict


def _get_path(data: dict, path: str):
    current = data
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _as_number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _winner(value_a, value_b, higher_is_better: bool) -> str:
    if value_a is None or value_b is None:
        return "tie"
    if value_a == value_b:
        return "tie"
    if higher_is_better:
        return "playerA" if value_a > value_b else "playerB"
    return "playerA" if value_a < value_b else "playerB"


class ComparisonService:
    def __init__(self):
        self.metrics = [
            {"key": "win_rate", "label": "Win Rate", "category": "Overall", "path": "profile.winrate", "unit": "", "higherIsBetter": True},
            {"key": "total_matches", "label": "Total Matches", "category": "Overall", "path": "profile.total_matches", "unit": "", "higherIsBetter": True},
            {"key": "aim_rating", "label": "Aim Rating", "category": "Aim", "path": "profile.rating.aim", "unit": "", "higherIsBetter": True},
            {"key": "utility_rating", "label": "Utility Rating", "category": "Utility", "path": "profile.rating.utility", "unit": "", "higherIsBetter": True},
            {"key": "clutch_rating", "label": "Clutch Rating", "category": "Clutch", "path": "profile.rating.clutch", "unit": "", "higherIsBetter": True},
            {"key": "opening_rating", "label": "Opening Rating", "category": "Entry", "path": "profile.rating.opening", "unit": "", "higherIsBetter": True},
            {"key": "headshot_accuracy", "label": "Headshot Accuracy", "category": "Aim", "path": "profile.stats.accuracy_head", "unit": "", "higherIsBetter": True},
            {"key": "accuracy_enemy_spotted", "label": "Accuracy vs Spotted", "category": "Aim", "path": "profile.stats.accuracy_enemy_spotted", "unit": "", "higherIsBetter": True},
            {"key": "trade_kills_success", "label": "Trade Kills Success", "category": "Teamplay", "path": "profile.stats.trade_kills_success_percentage", "unit": "", "higherIsBetter": True},
            {"key": "traded_deaths_success", "label": "Traded Deaths Success", "category": "Teamplay", "path": "profile.stats.traded_deaths_success_percentage", "unit": "", "higherIsBetter": True},
            {"key": "ct_opening_duel", "label": "CT Opening Duel", "category": "Entry", "path": "profile.stats.ct_opening_duel_success_percentage", "unit": "", "higherIsBetter": True},
            {"key": "t_opening_duel", "label": "T Opening Duel", "category": "Entry", "path": "profile.stats.t_opening_duel_success_percentage", "unit": "", "higherIsBetter": True},
        ]

    def compare(self, player_a: dict, player_b: dict) -> dict:
        normalized = []
        category_wins = defaultdict(lambda: {"playerA": 0, "playerB": 0})

        for metric in self.metrics:
            value_a = _as_number(_get_path(player_a, metric["path"]))
            value_b = _as_number(_get_path(player_b, metric["path"]))
            if value_a is None or value_b is None:
                continue

            winner = _winner(value_a, value_b, metric["higherIsBetter"])
            if winner in {"playerA", "playerB"}:
                category_wins[metric["category"]][winner] += 1

            normalized.append(
                {
                    "key": metric["key"],
                    "label": metric["label"],
                    "category": metric["category"],
                    "playerAValue": value_a,
                    "playerBValue": value_b,
                    "unit": metric["unit"],
                    "higherIsBetter": metric["higherIsBetter"],
                    "winner": winner,
                }
            )

        summary = []
        for category, wins in category_wins.items():
            if wins["playerA"] == wins["playerB"]:
                summary.append(f"Both players are even in {category.lower()} metrics.")
            elif wins["playerA"] > wins["playerB"]:
                summary.append(f"Player A leads in {category.lower()} metrics.")
            else:
                summary.append(f"Player B leads in {category.lower()} metrics.")

        return {"stats": normalized, "summary": summary}
