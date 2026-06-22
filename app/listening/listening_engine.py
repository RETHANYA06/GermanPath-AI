import random
from app.listening.listening_loader import load_listening_files


def get_random_listening():

    files = load_listening_files()

    text = random.choice(files)

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    transcript = []
    question = ""
    options = []
    answer = ""

    mode = "transcript"

    for line in lines:

        if line == "QUESTION:":
            mode = "question"
            continue

        if line == "OPTIONS:":
            mode = "options"
            continue

        if line == "ANSWER:":
            mode = "answer"
            continue

        if mode == "transcript":
            transcript.append(line)

        elif mode == "question":
            question = line

        elif mode == "options":
            options.append(line)

        elif mode == "answer":
            answer = line

    return {
        "transcript": "\n".join(transcript),
        "question": question,
        "options": options,
        "answer": answer
    }