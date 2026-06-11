import random

from app.data.content_loader import load_vocabulary_topics


def get_flashcard():

    words = load_vocabulary_topics()

    return random.choice(words)