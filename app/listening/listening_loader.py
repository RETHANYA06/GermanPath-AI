from pathlib import Path


def load_listening_files():

    folder = Path("content/A1/listening")

    listening_files = []

    for file in folder.glob("*.txt"):

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:

            listening_files.append(
                f.read()
            )

    return listening_files