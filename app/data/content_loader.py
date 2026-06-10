from pathlib import Path

VOCAB_FOLDER = Path("content/A1/vocabulary")


def load_vocabulary_topics():
    vocabulary = []

    if not VOCAB_FOLDER.exists():
        return vocabulary

    for file in VOCAB_FOLDER.glob("*.md"):

        topic = file.stem.replace("_", " ").title()

        with open(file, "r", encoding="utf-8") as f:

            for line in f:

                line = line.strip()

                if (
                    not line
                    or line.startswith("#")
                    or "=" not in line
                ):
                    continue

                german, english = line.split("=", 1)

                vocabulary.append({
                    "topic": topic,
                    "german": german.strip(),
                    "english": english.strip()
                })

    return vocabulary