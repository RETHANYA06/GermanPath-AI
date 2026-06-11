from app.quizzes.quiz_engine import generate_question


def initialize_quiz(total_questions):

    return {
        "current": 1,
        "total": total_questions,
        "score": 0,
        "question": generate_question(),
        "answered": False
    }