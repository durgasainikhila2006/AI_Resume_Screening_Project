from flask import Flask, render_template, request, redirect
from database import save_candidate, get_all_candidates, delete_candidate
from resume_parser import parse_resume
from datetime import datetime
import os

app = Flask(__name__)

# -----------------------------
# Upload Folder
# -----------------------------
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Resume Prediction
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():

    if "resume" not in request.files:
        return "No file uploaded."

    file = request.files["resume"]

    if file.filename == "":
        return "Please select a resume."

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    # -----------------------------
    # Parse Resume
    # -----------------------------
    resume = parse_resume(filepath)

    name = resume["name"]
    email = resume["email"]
    phone = resume["phone"]
    education = resume["education"]
    experience = resume["experience"]
    skills = resume["skills"]
    project_count = resume["project_count"]
    certifications = resume["certifications"]
    github = resume["github"]
    resume_text = resume["resume_text"]

    text = resume_text.lower()

    # -----------------------------
    # Keywords
    # -----------------------------
    education_keywords = [
        "b.sc","bsc","b.tech","btech",
        "m.sc","msc","m.tech","mtech",
        "degree","graduate","bachelor"
    ]

    skill_keywords = [
        "python","sql","excel","power bi",
        "tableau","machine learning",
        "data analysis","pandas","numpy",
        "java","c++","html","css",
        "javascript","ms office",
        "google sheets",
        "communication",
        "problem solving"
    ]

    experience_keywords = [
        "experience",
        "internship",
        "intern",
        "project"
    ]

    certificate_keywords = [
        "certificate",
        "certification",
        "certified"
    ]

    # -----------------------------
    # Resume Score
    # -----------------------------
    score = 0

    if any(word in text for word in education_keywords):
        score += 20

    skills_found = [
        skill for skill in skill_keywords
        if skill in text
    ]

    score += min(len(skills_found) * 8, 40)

    if any(word in text for word in experience_keywords):
        score += 20

    if any(word in text for word in certificate_keywords):
        score += 10

    if email != "Not Found":
        score += 5

    if phone != "Not Found":
        score += 5

    score = min(score, 100)

    # -----------------------------
    # Skill Match
    # -----------------------------
    total_skills = len(skill_keywords)
    matched_skills = len(skills_found)

    skill_percentage = int(
        (matched_skills / total_skills) * 100
    )

    # -----------------------------
    # ATS Score
    # -----------------------------
    ats_score = int(
        (score + skill_percentage) / 2
    )

    # -----------------------------
    # Prediction
    # -----------------------------
    if score >= 70 and ats_score >= 60:
        prediction = "Shortlisted"
    else:
        prediction = "Not Shortlisted"

    # -----------------------------
    # Upload Time
    # -----------------------------
    upload_time = datetime.now()

    # -----------------------------
    # Save Candidate
    # -----------------------------
    save_candidate(
        filename=file.filename,
        name=name,
        email=email,
        phone=phone,
        education=education,
        experience=experience,
        resume_score=score,
        skill_match=skill_percentage,
        prediction=prediction,
        upload_time=upload_time
    )

    # -----------------------------
    # Result Page
    # -----------------------------
    return render_template(
        "result.html",
        filename=file.filename,
        name=name,
        email=email,
        phone=phone,
        education=education,
        experience=experience,
        skills=skills_found,
        score=score,
        ats_score=ats_score,
        project_count=project_count,
        certifications=certifications,
        github=github,
        skill_percentage=skill_percentage,
        prediction=prediction,
        upload_time=upload_time.strftime("%d-%m-%Y %I:%M %p")
    )


# -----------------------------
# Dashboard
# -----------------------------
from database import (
    save_candidate,
    get_all_candidates,
    delete_candidate,
    get_total_candidates,
    get_shortlisted_count,
    get_rejected_count,
    get_average_score
)

@app.route("/dashboard")
def dashboard():

    return render_template(
        "dashboard.html",
        candidates=get_all_candidates(),
        total=get_total_candidates(),
        shortlisted=get_shortlisted_count(),
        rejected=get_rejected_count(),
        average=get_average_score()
    )


# -----------------------------
# Delete Candidate
# -----------------------------
@app.route("/delete/<int:id>")
def delete(id):

    delete_candidate(id)

    return redirect("/dashboard")


# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)