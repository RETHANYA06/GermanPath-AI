import random

from app.data.a1_dictionary import A1_DICTIONARY


def generate_question():

    german_word = random.choice(
        list(A1_DICTIONARY.keys())
    )

    correct_answer = A1_DICTIONARY[german_word]

    wrong_answers = []

    while len(wrong_answers) < 3:

        candidate = random.choice(
            list(A1_DICTIONARY.values())
        )

        if (
            candidate != correct_answer
            and candidate not in wrong_answers
        ):
            wrong_answers.append(candidate)

    options = wrong_answers + [correct_answer]

    random.shuffle(options)

    return {
        "word": german_word,
        "correct": correct_answer,
        "options": options
    }