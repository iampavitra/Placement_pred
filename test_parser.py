import io
import PyPDF2
from src.resume_parser import parse_resume_to_features

class MockPage:
    def extract_text(self):
        return "Jane Doe. B.Tech Computer Science. CGPA 9.2. Python, Java. Internship at Microsoft as Software Engineer Intern. Project: Automated Placement Prediction System (Machine Learning)."

class MockReader:
    pages = [MockPage()]

# Mock the reader
PyPDF2.PdfReader = lambda x: MockReader()

print(parse_resume_to_features(io.BytesIO(b"dummy")))
