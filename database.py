import mysql.connector

# -----------------------------
# Database Connection
# -----------------------------
def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Sainikhila2006",
        database="resume_screening"
    )

# -----------------------------
# Save Candidate
# -----------------------------
def save_candidate(filename, name, email, phone, education,
                   experience, resume_score, skill_match,
                   prediction, upload_time):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO candidates
    (filename, name, email, phone, education,
     experience, resume_score, skill_match,
     prediction, upload_time)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        filename,
        name,
        email,
        phone,
        education,
        experience,
        resume_score,
        skill_match,
        prediction,
        upload_time
    )

    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

# -----------------------------
# Get All Candidates
# -----------------------------
def get_all_candidates():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM candidates
        ORDER BY upload_time DESC
    """)

    candidates = cursor.fetchall()

    cursor.close()
    conn.close()

    return candidates
def get_total_candidates():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM candidates")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total


def get_shortlisted_count():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM candidates WHERE prediction='Shortlisted'")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total


def get_rejected_count():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM candidates WHERE prediction='Not Shortlisted'")
    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total


def get_average_score():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(resume_score) FROM candidates")
    avg = cursor.fetchone()[0]

    if avg is None:
        avg = 0

    cursor.close()
    conn.close()

    return round(avg, 1)
# -----------------------------
# Delete Candidate
# -----------------------------
def delete_candidate(candidate_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM candidates WHERE id=%s",
        (candidate_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()