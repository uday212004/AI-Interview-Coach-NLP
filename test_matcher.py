from src.matcher import RoleMatcher

skills = [
    "python",
    "sql",
    "excel"
]

matcher = RoleMatcher()

result = matcher.calculate_match(
    skills,
    "Data Analyst"
)

print(result)

print(
    matcher.generate_insight(
        result["score"]
    )
)