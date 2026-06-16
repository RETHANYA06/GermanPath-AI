import random

from app.reading.reading_loader import load_readings


def parse_reading(text):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    title = ""
    passage_lines = []

    question = ""
    options = []
    answer = ""

    if lines and lines[0].startswith("#"):
        title = lines[0].replace("#", "").strip()

    try:

        fragen_index = lines.index("Fragen:")

        passage_lines = lines[1:fragen_index]

        question = lines[fragen_index + 1]

        options = [
            lines[fragen_index + 2],
            lines[fragen_index + 3],
            lines[fragen_index + 4],
            lines[fragen_index + 5]
        ]

        answer = options[0]

    except Exception:
        pass

    return {
        "title": title,
        "passage": "\n".join(passage_lines),
        "question": question,
        "options": options,
        "answer": answer
    }


def get_random_reading():

    readings = load_readings()

    raw = random.choice(readings)

    return parse_reading(raw)