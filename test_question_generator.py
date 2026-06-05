from src.question_generator import QuestionGenerator

generator = QuestionGenerator()

questions = generator.get_questions(
    "Data Analyst",
    "Medium",
    "Technical"
)

for question in questions:
    print(question)