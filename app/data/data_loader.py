from pathlib import Path

VOCAB_PATH = Path("datasets/vocabulary/de_50k.txt")
SENTENCE_PATH = Path("datasets/sentences/deu.txt")


def load_vocabulary(limit=100):
    words = []

    if not VOCAB_PATH.exists():
        return words

    with open(VOCAB_PATH, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 1:
                words.append(parts[0])

            if len(words) >= limit:
                break

    return words


def load_sentences(limit=100):
    sentences = []

    if not SENTENCE_PATH.exists():
        return sentences

    with open(SENTENCE_PATH, "r", encoding="utf-8") as file:
        for line in file:
            sentences.append(line.strip())

            if len(sentences) >= limit:
                break

    return sentences