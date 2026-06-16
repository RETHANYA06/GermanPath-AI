import json
import os

PROGRESS_FILE = "user_progress.json"


def load_progress():

    if os.path.exists(PROGRESS_FILE):

        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)

    return {
        "quiz_correct": 0,
        "quiz_total": 0,
        "reading_correct": 0,
        "reading_total": 0,
        "grammar_correct": 0,
        "grammar_total": 0
    }


def save_progress(progress):

    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=4)