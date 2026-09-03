from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

@app.route("/health")
def health():
   return {"status": "healthy","version":"v3"}, 200

def get_db_connection():
    return mysql.connector.connect(
        host="mysql",
        user="root",
        password="root",
        database="student_db"
    )



@app.route("/students", methods=["GET"])
def get_students():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT id,name,age FROM students")

    students = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(students)



@app.route("/students", methods=["POST"])
def add_student():

    data = request.get_json()

    name = data["name"]
    age = data["age"]

    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO students (name, age) VALUES (%s, %s)",
        (name, age)
    )

    db.commit()

    student_id = cursor.lastrowid

    cursor.close()
    db.close()

    return jsonify({
        "id": student_id,
        "name": name,
        "age": age
    }), 201



@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, name, age FROM students WHERE id = %s",
        (id,)
    )

    student = cursor.fetchone()

    cursor.close()
    db.close()

    if student:
        return jsonify(student)

    return jsonify({"message": "Student not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
