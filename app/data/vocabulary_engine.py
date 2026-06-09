from data.data_loader import load_vocabulary


def get_a1_words(limit=20):
    words = load_vocabulary(limit)
    return words