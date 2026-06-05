from src.skill_extractor import SkillExtractor

extractor = SkillExtractor()

sample_text = """
Python Python Python
SQL SQL
Power BI
Pandas
Machine Learning
"""

skills = extractor.extract_skills(sample_text)

frequency = extractor.skill_frequency(sample_text)

print("Skills:")
print(skills)

print("\nFrequency:")
print(frequency)