from src.evaluator import AnswerEvaluator

evaluator = AnswerEvaluator()

question = "Explain SQL JOINs"

answer = """
SQL JOINs combine data from
multiple tables using common
columns.
INNER JOIN returns matching
records.
LEFT JOIN returns all records
from left table.
"""

result = evaluator.evaluate_answer(
    question,
    answer
)

print(result)