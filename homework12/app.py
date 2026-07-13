from flask import Flask, abort, request, jsonify
import csv

app = Flask(__name__)

# ===== HELPER FUNCTIONS =====

def read_students():
    students = []
    try:
        with open("students.csv", mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append(row)
    except FileNotFoundError:
        pass
    return students

def write_students(students):

    with open("students.csv", mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "surname", "age"])
        writer.writeheader()
        writer.writerows(students)

def row_to_dict(row):
    return {
        "id": int(row['id']),
        "name": row['name'],
        "surname": row['surname'],
        "age": int(row['age'])
    }

def validate_age(age):
    try:
        age = int(age)
    except (TypeError, ValueError):
        abort(400, description="Age must be an integer.")
    
    if age < 0:
        abort(400, description="Age cannot be negative.")
    
    return age

def get_request_data():
    return request.get_json(silent=True) or request.form

def validate_fields(data, required_fields, allowed_fields):
    received_fields = set(data.keys())

    missing_fields = required_fields - received_fields
    extra_fields = received_fields - allowed_fields

    if missing_fields:
        abort(400, description=f"Provide name, surname, and age. Missing fields: {', '.join(missing_fields)}")
    
    if extra_fields:
        abort(400, description=f"Provide only name, surname, and age. Extra fields: {', '.join(extra_fields)}")

@app.route("/")
def hello_world():
    return "Hello "

@app.route("/students")
def students():
    student_list = [row_to_dict(row) for row in read_students()]
    return jsonify(student_list)

@app.route("/students/<string:student_surname>")
def student_by_surname(student_surname):
    students = [row_to_dict(row) for row in read_students() if row['surname'] == student_surname]
    
    if students:
        return jsonify(students)
    abort(404, description="No student with this surname.")

@app.route("/student/<int:student_id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def student(student_id):
    match request.method:
        case "GET":
            for row in read_students():
                if int(row['id']) == student_id:
                    return jsonify(row_to_dict(row))
            abort(404, description="No student with this ID.")
        
        case "PUT":
            data = get_request_data()
            required_fields = {"name", "surname", "age"}
            allowed_fields = {"name", "surname", "age"}

            validate_fields(data, required_fields, allowed_fields)

            if not data or not all(key in data for key in ("name", "surname", "age")):
                abort(400, description="Missing student data. Provide name, surname, and age.")
            
            age = validate_age(data["age"])
            
            students = read_students()
            target_student = None
            for row in students:
                if int(row['id']) == student_id:
                    found = True
                    row["name"] = data["name"]
                    row["surname"] = data["surname"]
                    row["age"] = str(age)
                    target_student = row
                    break
            
            if target_student is None:
                abort(404, description="No student with this ID.")
            
            write_students(students)
            return jsonify(target_student), 200
        
        case "PATCH":
            data = get_request_data()
            allowed_fields = {"age"}
            required_fields = {"age"}

            validate_fields(data, required_fields, allowed_fields)

            if not data or "age" not in data:
                abort(400, description="Missing student data. Provide age.")
            
            age = validate_age(data["age"])
            
            students = read_students()
            target_student = None
            for row in students:
                if int(row['id']) == student_id:
                    found = True
                    row["age"] = str(age)
                    target_student = row
                    break
            
            if target_student is None:
                abort(404, description="No student with this ID.")
            
            write_students(students)
            return jsonify(target_student), 200
      
        case "DELETE":
            students = read_students()
            found = False
            filtered_students = []
            
            for row in students:
                if int(row['id']) == student_id:
                    found = True
                else:
                    filtered_students.append(row)
            
            if not found:
                abort(404, description="No student with this ID.")
            
            write_students(filtered_students)
            return jsonify(filtered_students), 200

@app.route("/student", methods=["POST"])
def create_student():
    data = get_request_data()

    required_fields = {"name", "surname", "age"}
    allowed_fields = {"name", "surname", "age"}

    validate_fields(data, required_fields, allowed_fields)
    
    age = validate_age(data["age"])
    
    # Find max ID
    students = read_students()
    max_id = max((int(row['id']) for row in students), default=0)
    
    new_student = {
        "id": str(max_id + 1),
        "name": data["name"],
        "surname": data["surname"],
        "age": str(age),
    }
    
    students.append(new_student)
    write_students(students)
    
    return jsonify(new_student), 201

if __name__ == "__main__":
    app.run(debug=True)