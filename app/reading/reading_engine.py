import random

from app.reading.reading_loader import load_readings


def parse_reading(text):

    lines = text.splitlines()

    title = ""
    passage_lines = []
    question = ""
    options = []
    answer = ""

    mode = None

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line.startswith("TITLE:"):
            title = line.replace("TITLE:", "").strip()
            mode = None

        elif line.startswith("PASSAGE:"):
            mode = "passage"

        elif line.startswith("QUESTION:"):
            mode = "question"

        elif line.startswith("OPTIONS:"):
            mode = "options"

        elif line.startswith("ANSWER:"):
            mode = "answer"

        else:

            if mode == "passage":
                passage_lines.append(line)

            elif mode == "question":
                question = line

            elif mode == "options":
                options.append(line)

            elif mode == "answer":
                answer = line

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