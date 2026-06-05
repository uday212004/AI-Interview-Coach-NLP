from src.parser import ResumeParser

parser = ResumeParser()

text = parser.extract_text("resumes/resume.pdf")

print(text)