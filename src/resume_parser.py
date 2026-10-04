import re
import PyPDF2

def parse_resume_to_features(file_stream):
    """
    Takes a file stream (PDF), extracts text, and uses regex/heuristics
    to map resume content to the 9 ML model features.
    """
    text = ""
    try:
        reader = PyPDF2.PdfReader(file_stream)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + " "
    except Exception as e:
        return {"error": str(e)}

    if not text.strip():
        return {"error": "Could not extract text from PDF."}

    text_lower = text.lower()

    # 1. CGPA Extraction
    cgpa = 7.0  # default
    cgpa_matches = re.findall(r'cgpa[\s:]*([0-9]\.[0-9]+|10\.0+)', text_lower)
    if cgpa_matches:
        try:
            parsed_cgpa = float(cgpa_matches[0])
            if 0.0 <= parsed_cgpa <= 10.0:
                cgpa = parsed_cgpa
        except:
            pass

    # 2. 10th Percentage
    tenth = 75.0 # default
    tenth_matches = re.findall(r'(?:10th|x\s|secondary).*?([0-9]{2,3}(?:\.[0-9]+)?)[\s]*%', text_lower)
    if tenth_matches:
        try:
            parsed = float(tenth_matches[0])
            if 0.0 <= parsed <= 100.0:
                tenth = parsed
        except:
            pass

    # 3. 12th Percentage
    twelfth = 75.0
    twelfth_matches = re.findall(r'(?:12th|xii\s|higher secondary).*?([0-9]{2,3}(?:\.[0-9]+)?)[\s]*%', text_lower)
    if twelfth_matches:
        try:
            parsed = float(twelfth_matches[0])
            if 0.0 <= parsed <= 100.0:
                twelfth = parsed
        except:
            pass

    # 4. Internships (count occurrences of "intern" or "internship")
    intern_count = len(re.findall(r'\binternship\b|\bintern\b', text_lower))
    internships = min(intern_count, 5)

    # 5. Projects (count occurrences of "project")
    proj_count = len(re.findall(r'\bproject\b', text_lower))
    projects = min(proj_count, 5)

    # 6. Technical Skills (1-5 scale)
    tech_keywords = ['python', 'java', 'c++', 'javascript', 'react', 'sql', 'machine learning', 'html', 'css', 'node', 'aws']
    tech_score = sum(1 for kw in tech_keywords if kw in text_lower)
    # Map score: 0->1, 1-2->2, 3-4->3, 5-6->4, 7+->5
    if tech_score == 0:
        tech_level = 1
    elif tech_score <= 2:
        tech_level = 2
    elif tech_score <= 4:
        tech_level = 3
    elif tech_score <= 6:
        tech_level = 4
    else:
        tech_level = 5

    # 7. Communication Skills (1-5 scale)
    comm_keywords = ['communication', 'team', 'lead', 'presented', 'organized', 'managed', 'coordinated', 'english']
    comm_score = sum(1 for kw in comm_keywords if kw in text_lower)
    if comm_score == 0:
        comm_level = 2 # generous default
    elif comm_score <= 2:
        comm_level = 3
    elif comm_score <= 4:
        comm_level = 4
    else:
        comm_level = 5

    # 8. Work Experience (Yes/No)
    exp_keywords = ['experience', 'work history', 'employment', 'employed', 'full-time', 'freelance']
    has_experience = any(kw in text_lower for kw in exp_keywords)
    work_exp = 'Yes' if has_experience else 'No'

    # 9. Backlogs
    backlog_count = 0
    if 'backlog' in text_lower:
        bl_matches = re.findall(r'([0-9]+)\s*backlog', text_lower)
        if bl_matches:
            backlog_count = int(bl_matches[0])
        else:
            backlog_count = 1 # found word but no number

    return {
        "success": True,
        "features": {
            "cgpa": cgpa,
            "tenth_percentage": tenth,
            "twelfth_percentage": twelfth,
            "internships": internships,
            "projects": projects,
            "technical_skills": tech_level,
            "communication_skills": comm_level,
            "backlogs": backlog_count,
            "work_experience": work_exp
        }
    }
