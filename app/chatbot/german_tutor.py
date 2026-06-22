def ask_tutor(question):

    question = question.lower()

    if "akkusativ" in question:
        return """
Akkusativ is used for the direct object.

Example:
Ich kaufe den Apfel.
(I buy the apple)

'den Apfel' is Akkusativ.
"""

    elif "dativ" in question:
        return """
Dativ is used for the indirect object.

Example:
Ich gebe dem Mann ein Buch.
(I give the man a book)

'dem Mann' is Dativ.
"""

    elif "der die das" in question:
        return """
der = masculine
die = feminine
das = neuter
"""

    else:
        return """
Sorry, I don't know that yet.
Try asking about:
- Akkusativ
- Dativ
- der die das
"""