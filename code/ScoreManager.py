import json
import os

SCORE_FILE = "scores.json"


def load_scores():
    if not os.path.exists(SCORE_FILE):
        return []

    try:
        with open(SCORE_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_scores(scores_list):
    with open(SCORE_FILE, 'w') as f:
        json.dump(scores_list, f, indent=4)


def add_score(new_score: dict):
    scores = load_scores()
    scores.append(new_score)
    scores.sort(key=lambda s: s['kills'], reverse=True)
    save_scores(scores)