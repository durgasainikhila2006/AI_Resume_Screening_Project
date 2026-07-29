import pdfplumber
import docx
import re

# -----------------------------------------
# Skills List
# -----------------------------------------
SKILLS = [

    # Programming
    "Python","Java","C","C++","R","SQL",

    # Web
    "HTML","CSS","JavaScript","Flask","Django",

    # Data Science
    "Machine Learning",
    "Deep Learning",
    "Pandas",
    "NumPy",
    "TensorFlow",
    "Power BI",
    "Tableau",
    "Excel",

    # Office
    "MS Office",
    "Google Sheets",

    # Soft Skills
    "Communication",
    "Problem Solving",
    "Problem-solving",
    "Leadership",
    "Teamwork",
    "Fast Learner",
    "Self Motivated",
    "Self-Motivated",
    "Multitasking",
    "Critical Thinking",

    # Tools
    "Git",
    "GitHub",
    "LinkedIn"
]


# -----------------------------------------
# Read Resume
# -----------------------------------------
def extract_text(file_path):

    text = ""

    if file_path.lower().endswith(".pdf"):

        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:

                    text += page_text + "\n"

    elif file_path.lower().endswith(".docx"):

        doc = docx.Document(file_path)

        for para in doc.paragraphs:

            text += para.text + "\n"

    return text


# -----------------------------------------
# Name
# -----------------------------------------
def extract_name(text):

    for line in text.split("\n"):

        line = line.strip()

        if len(line.split()) >= 2 and len(line) < 40:

            if not any(word in line.lower() for word in
                ["email","phone","github","linkedin","resume"]):

                return line

    return "Not Found"


# -----------------------------------------
# Email
# -----------------------------------------
def extract_email(text):

    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    return match.group() if match else "Not Found"


# -----------------------------------------
# Phone
# -----------------------------------------
def extract_phone(text):

    match = re.search(
        r"(\+91[- ]?)?[6-9]\d{9}",
        text
    )

    return match.group() if match else "Not Found"


# -----------------------------------------
# Skills
# -----------------------------------------
def extract_skills(text):

    skills = []

    for skill in SKILLS:

        if re.search(
            r"\b" + re.escape(skill) + r"\b",
            text,
            re.IGNORECASE
        ):
            skills.append(skill)

    return list(set(skills))


# -----------------------------------------
# Education
# -----------------------------------------
def extract_education(text):

    education_keywords = [

        "Bachelor",
        "B.Sc",
        "BSC",
        "B.Tech",
        "BCA",
        "M.Sc",
        "MCA",
        "MBA",
        "M.Tech",
        "Degree",
        "Diploma"

    ]

    for line in text.split("\n"):

        for word in education_keywords:

            if word.lower() in line.lower():

                return line.strip()

    return "Not Found"


# -----------------------------------------
# Experience
# -----------------------------------------
def extract_experience(text):

    year = re.search(
        r"(\d+)\+?\s*(year|years)",
        text,
        re.IGNORECASE
    )

    if year:

        return year.group()

    month = re.search(
        r"(\d+)\+?\s*(month|months)",
        text,
        re.IGNORECASE
    )

    if month:

        return month.group()

    if "internship" in text.lower():

        return "Internship"

    return "Fresher"


# -----------------------------------------
# Parse Resume
# -----------------------------------------
def parse_resume(file_path):

    text = extract_text(file_path)

    skills = extract_skills(text)

    result = {

        "name": extract_name(text),

        "email": extract_email(text),

        "phone": extract_phone(text),

        "education": extract_education(text),

        "experience": extract_experience(text),

        "skills": skills,

        "project_count": len(
            re.findall(
                r"\bproject\b",
                text,
                re.IGNORECASE
            )
        ),

        "certifications": len(
            re.findall(
                r"\b(certification|certificate|certified)\b",
                text,
                re.IGNORECASE
            )
        ),

        "github": 1 if "github" in text.lower() else 0,

        "resume_score": min(len(skills) * 8,100),

        "resume_text": text

    }

    return result