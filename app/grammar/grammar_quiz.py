import random

QUESTIONS = [

    {
        "question": "What is the article for Mann?",
        "options": [
            "Der",
            "Die",
            "Das",
            "Den"
        ],
        "answer": "Der"
    },

    {
        "question": "What is the article for Frau?",
        "options": [
            "Der",
            "Die",
            "Das",
            "Den"
        ],
        "answer": "Die"
    },

    {
        "question": "What is the article for Kind?",
        "options": [
            "Der",
            "Die",
            "Das",
            "Den"
        ],
        "answer": "Das"
    },

    {
        "question": "Ich means?",
        "options": [
            "I",
            "You",
            "He",
            "She"
        ],
        "answer": "I"
    },

    {
        "question": "Du means?",
        "options": [
            "I",
            "You",
            "We",
            "They"
        ],
        "answer": "You"
    }

]

def get_grammar_question():

    return random.choice(
        QUESTIONS
    )