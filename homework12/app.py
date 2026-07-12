from flask import Flask, abort, request, jsonify
import csv

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello "

@app.route("/students")
def students():
      with open("students.csv", mode="r", encoding="utf-8") as file:
        # Initialize the DictReader object
        reader = csv.DictReader(file)
        # Iterate through rows; each row is a standard Python dictionary
        student_list = []
        for row in reader:
            student_list.append({
                "id": int(row['id']),
                "name": row['name'],
                "surname": row['surname'],
                "age": int(row['age'])
            })
        return jsonify(student_list)

@app.route("/students/<string:student_surname>")
def student_by_surname(student_surname):
    print(f"DEBUG: Searching for surname: '{student_surname}'")
    students = []
    with open("students.csv", mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(f"DEBUG: Comparing CSV surname '{row['surname']}' with requested '{student_surname}'")
            if row['surname'] == student_surname:
                students.append({
                    "id": int(row['id']),
                    "name": row['name'],
                    "surname": row['surname'],
                    "age": int(row['age'])
                })

    if students:
        return jsonify(students)
    abort(404, description="No student with this surname.")

@app.route("/student/<int:student_id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def student(student_id):
    match request.method:
        case "GET":
            with open("students.csv", mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if int(row['id']) == student_id:
                        return jsonify({
                            "id": int(row['id']),
                            "name": row['name'],
                            "surname": row['surname'],
                            "age": int(row['age'])
                        })
            abort(404, description="No student with this ID.")
        
        case "PUT":
            data = request.get_json(silent=True) or request.form
            if not data or not all(key in data for key in ("name", "surname", "age")):
                abort(400, description="Missing student data. Provide name, surname, and age.")
            try:
                age = int(data["age"])
            except (TypeError, ValueError):
                abort(400, description="Age must be an integer.")

            if age < 0:
                abort(400, description="Age cannot be negative.")

            remaining_students = []
            found = False
            with open("students.csv", mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if int(row['id']) == student_id:
                        found = True
                        updated_student = {
                            "id": str(student_id),
                            "name": data["name"],
                            "surname": data["surname"],
                            "age": str(data["age"]),
                        }
                        remaining_students.append(updated_student)
                    else:
                        remaining_students.append(row)
            
            if not found:
                abort(404, description="No student with this ID.")
            
            # Rewrite CSV without deleted student
            with open("students.csv", mode="w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["id", "name", "surname", "age"])
                writer.writeheader()
                writer.writerows(remaining_students)
            return jsonify({"message": f"Student with ID {student_id} updated successfully"}), 200
        
        case "PATCH":
            data = request.get_json(silent=True) or request.form

            if not data or "age" not in data:
                abort(400, description="Missing student data. Provide age.")
            try:
                age = int(data["age"])
            except (TypeError, ValueError):
                abort(400, description="Age must be an integer.")

            if age < 0:
                abort(400, description="Age cannot be negative.")


            remaining_students = []
            found = False

            with open("students.csv", mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    if int(row["id"]) == student_id:
                        found = True
                        row["age"] = str(age)
                    remaining_students.append(row)

            if not found:
                abort(404, description="No student with this ID.")

            with open("students.csv", mode="w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(
                file,
                fieldnames=["id", "name", "surname", "age"]
             )
                writer.writeheader()
                writer.writerows(remaining_students)

            return jsonify({
                "message": f"Student with ID {student_id} partially updated successfully"
                }), 200
      
        case "DELETE":
            # Read all students except the one to delete
            remaining_students = []
            found = False
            with open("students.csv", mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if int(row['id']) == student_id:
                        found = True
                    else:
                        remaining_students.append(row)
            
            if not found:
                abort(404, description="No student with this ID.")
            
            # Rewrite CSV without deleted student
            with open("students.csv", mode="w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["id", "name", "surname", "age"])
                writer.writeheader()
                writer.writerows(remaining_students)
            
            return jsonify({"message": f"Student with ID {student_id} deleted successfully"}), 200

@app.route("/student", methods=["POST"])
def create_student():
    data = request.get_json(silent=True) or request.form

    if not data or not all(key in data for key in ("name", "surname", "age")):
        abort(
            400,
            description="Missing student data. Provide name, surname, and age."
        )

    try:
        age = int(data["age"])
    except (TypeError, ValueError):
        abort(400, description="Age must be an integer.")

    if age < 0:
        abort(400, description="Age cannot be negative.")

    max_id = 0

    with open("students.csv", mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if int(row["id"]) > max_id:
                max_id = int(row["id"])

    new_student = {
        "id": str(max_id + 1),
        "name": data["name"],
        "surname": data["surname"],
        "age": str(age),
    }

    with open(
        "students.csv",
        mode="a",
        encoding="utf-8",
        newline=""
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["id", "name", "surname", "age"]
        )
        writer.writerow(new_student)

    return jsonify({
        "student": {
            "id": int(new_student["id"]),
            "name": new_student["name"],
            "surname": new_student["surname"],
            "age": int(new_student["age"])
        }
    }), 201

if __name__ == "__main__":
    app.run(debug=True)