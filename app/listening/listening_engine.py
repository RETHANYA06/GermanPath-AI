import random

from app.listening.listening_loader import (
    load_listening
)


def parse_listening(text):

    lines = text.splitlines()

    title = ""
    audio_text = ""
    question = ""
    options = []
    answer = ""

    mode = None

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if line.startswith("TITLE:"):
            title = line.replace(
                "TITLE:",
                ""
            ).strip()

        elif line.startswith("AUDIO_TEXT:"):
            mode = "audio"

        elif line.startswith("QUESTION:"):
            mode = "question"

        elif line.startswith("OPTIONS:"):
            mode = "options"

        elif line.startswith("ANSWER:"):
            mode = "answer"

        else:

            if mode == "audio":
                audio_text += line + "\n"

            elif mode == "question":
                question = line

            elif mode == "options":
                options.append(line)

            elif mode == "answer":
                answer = line

    return {
        "title": title,
        "audio_text": audio_text,
        "question": question,
        "options": options,
        "answer": answer
    }


def get_random_listening():

    lessons = load_listening()

    return parse_listening(
        random.choice(lessons)
    )