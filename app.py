# Import Flask and tools for handling requests and JSON responses
from flask import Flask, request, jsonify

# Create Flask app
app = Flask(__name__)

# Store student data in memory (no database)
students = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "major": "CIS",
        "grades": [88, 92, 85],
        "status": "active"
    },
    {
        "id": 2,
        "name": "Brian Smith",
        "major": "Math",
        "grades": [70, 75, 80],
        "status": "active"
    },
    {
        "id": 3,
        "name": "Carla White",
        "major": "Biology",
        "grades": [50, 55, 58],
        "status": "active"
    },
    {
        "id": 4,
        "name": "David Lee",
        "major": "History",
        "grades": [95, 90, 93],
        "status": "inactive"
    },
    {
        "id": 5,
        "name": "Emma Brown",
        "major": "CS",
        "grades": [60, 67, 64],
        "status": "active"
    },
    {
        "id": 6,
        "name": "Frank Green",
        "major": "Physics",
        "grades": [40, 45, 50],
        "status": "active"
    }
]

# Test route to check if server is running
@app.route("/")
def home():
    return "Flask is working"

# POST: evaluate a student's performance
@app.route("/api/students/evaluate", methods=["POST"])
def evaluate_student():
    data = request.get_json()
    student_id = data.get("id")

    # find student by id
    student = None
    for s in students:
        if s["id"] == student_id:
            student = s
            break

    if not student:
        return jsonify({"error": "Student not found"}), 404

    # calculate average grade
    grades = student["grades"]
    avg = sum(grades) / len(grades)

    # determine pass or fail
    result = "pass" if avg >= 60 else "fail"

    return jsonify({
        "id": student["id"],
        "name": student["name"],
        "average": avg,
        "result": result
    })

from datetime import datetime

# PUT: update student grades with security check
@app.route("/api/students/update-grades", methods=["PUT"])
def update_grades():
    # get token from request header
    token = request.headers.get("Time-Access-Token")

    # set valid token and expiration date
    VALID_TOKEN = "abc123"
    EXPIRATION_DATE = datetime(2026, 6, 1)

    # check if token is missing
    if not token:
        return jsonify({"error": "Missing Time-Access-Token"}), 401

    # check if token is correct
    if token != VALID_TOKEN:
        return jsonify({"error": "Invalid token"}), 403

    # check if token is expired
    if datetime.now() > EXPIRATION_DATE:
        return jsonify({"error": "Token expired"}), 403

    # normal PUT logic continues
    data = request.get_json()
    student_id = data.get("id")
    new_grades = data.get("grades")

    for student in students:
        if student["id"] == student_id:
            student["grades"] = new_grades
            return jsonify({"message": "Grades updated successfully"})

    return jsonify({"error": "Student not found"}), 404

# GET: return summary analytics
@app.route("/api/students/analytics", methods=["GET"])
def analytics():
    total_students = len(students)
    active_students = 0
    inactive_students = 0
    passing_students = 0

    for student in students:
        # count active vs inactive
        if student["status"] == "active":
            active_students += 1
        else:
            inactive_students += 1

        # check if student is passing
        avg = sum(student["grades"]) / len(student["grades"])
        if avg >= 60:
            passing_students += 1

    return jsonify({
        "total_students": total_students,
        "active_students": active_students,
        "inactive_students": inactive_students,
        "passing_students": passing_students
    })



# Run the app
if __name__ == "__main__":
    app.run(debug=True)