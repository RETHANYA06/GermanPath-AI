import os

LISTENING_PATH = "content/A1/listening"


def load_listening():

    data = []

    for file in os.listdir(LISTENING_PATH):

        if file.endswith(".txt"):

            with open(
                os.path.join(
                    LISTENING_PATH,
                    file
                ),
                "r",
                encoding="utf-8"
            ) as f:

                data.append(
                    f.read()
                )

    return data