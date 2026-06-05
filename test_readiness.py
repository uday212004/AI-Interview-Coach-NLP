from src.readiness import ReadinessEngine

engine = ReadinessEngine()

result = engine.calculate_readiness(

    role_match_score=75,

    answer_score=85,

    extracted_skills=[
        "python",
        "sql",
        "excel"
    ],

    missing_skills=[
        "power bi",
        "statistics"
    ]
)

print(result)