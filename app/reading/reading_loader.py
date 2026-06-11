from pathlib import Path


def load_readings():

    readings = []

    reading_dir = Path("content/A1/reading")

    for file in reading_dir.glob("*.md"):

        with open(file, "r", encoding="utf-8") as f:

            readings.append(f.read())

    return readings