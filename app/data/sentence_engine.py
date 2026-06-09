from pathlib import Path

SENTENCE_PATH = Path("datasets/sentences/deu-eng/deu.txt")


def get_example_sentences(limit=10):
    sentences = []

    if not SENTENCE_PATH.exists():
        return sentences

    with open(SENTENCE_PATH, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split("\t")

            if len(parts) >= 2:
                english = parts[0]
                german = parts[1]

                sentences.append((german, english))

            if len(sentences) >= limit:
                break

    return sentences