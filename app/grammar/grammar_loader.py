import os

GRAMMAR_PATH = "content/A1/grammar"


def load_grammar_topics():

    topics = []

    for file in os.listdir(GRAMMAR_PATH):

        if file.endswith(".md"):

            topics.append(file)

    return sorted(topics)


def load_grammar_content(filename):

    path = os.path.join(
        GRAMMAR_PATH,
        filename
    )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()