import random

from app.data.content_loader import load_vocabulary_topics


def generate_question():

    words = load_vocabulary_topics()

    word = random.choice(words)

    correct = word["english"]

    wrong_answers = []

    while len(wrong_answers) < 3:

        candidate = random.choice(words)["english"]

        if (
            candidate != correct
            and candidate not in wrong_answers
        ):
            wrong_answers.append(candidate)

    options = wrong_answers + [correct]

    random.shuffle(options)

    return {
        "topic": word["topic"],
        "word": word["german"],
        "correct": correct,
        "options": options
    }