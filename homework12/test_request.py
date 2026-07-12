import requests
from faker import Faker

with open("results.txt", mode="w", encoding="utf-8") as results_file:
    results_file.write("Start performing test_request.py\n")

def log_message(message, results_file):
    with open("results.txt", mode="a", encoding="utf-8") as results_file:
        results_file.write(message + "\n")
    print(message + "\n")

def log_result(response, results_file):
    with open("results.txt", mode="a", encoding="utf-8") as results_file:
        results_file.write("Method: " + response.request.method + "\n")
        results_file.write("URL: " + response.url + "\n")
        results_file.write("Status Code: " + str(response.status_code) + "\n")
        results_file.write("Response: " + str(response.json()) + "\n")

    print("Method: " + response.request.method + "\n")
    print("URL: " + response.url + "\n")
    print("Status Code: " + str(response.status_code) + "\n")
    print("Response: " + str(response.json()) + "\n")

BASE_URL = "http://127.0.0.1:5000"
fake = Faker()

log_message(f"=== GET ALL STUDENTS ===", results_file)
response = requests.get(f"{BASE_URL}/students")
log_result(response, results_file)

update_age_target_customer_id =-1
update_target_customer_id = -1
delete_target_customer_id = -1
for i in range(3):
    new_student = {
        "name": fake.first_name(),
        "surname": fake.last_name(),
        "age": fake.random_int(min=18, max=30)
    }
    log_message(f"=== CREATE STUDENT ===", results_file)
    response = requests.post(f"{BASE_URL}/student", json=new_student)
    if i == 1:
        update_age_target_customer_id = response.json()["student"]["id"]
    if i == 2:
        update_target_customer_id = response.json()["student"]["id"]
    if i == 0:
        delete_target_customer_id = response.json()["student"]["id"]
    log_result(response, results_file)

log_message(f"=== GET ALL STUDENTS ===", results_file)
response = requests.get(f"{BASE_URL}/students")
log_result(response, results_file)

log_message(f"=== UPDATE AGE OF 2 STUDENTS ===", results_file)
response = requests.patch(f"{BASE_URL}/student/{update_age_target_customer_id}", json={"age": fake.random_int(min=18, max=30)})
log_result(response, results_file)

log_message(f"=== GET 2 STUDENT ===", results_file)
response = requests.get(f"{BASE_URL}/student/{update_age_target_customer_id}")
log_result(response, results_file)

log_message(f"=== UPDATE AGE OF 3 STUDENTS ===", results_file)
response = requests.put(f"{BASE_URL}/student/{update_target_customer_id}", json={"name": fake.first_name(), "surname": fake.last_name(), "age": fake.random_int(min=18, max=30)})
log_result(response, results_file)

log_message(f"=== GET 3 STUDENT ===", results_file)
response = requests.get(f"{BASE_URL}/student/{update_target_customer_id}")
log_result(response, results_file)

log_message(f"=== GET ALL STUDENTS ===", results_file)
response = requests.get(f"{BASE_URL}/students")
log_result(response, results_file)

log_message(f"=== DELETE 1 STUDENT ===", results_file)
response = requests.delete(f"{BASE_URL}/student/{delete_target_customer_id}")
log_result(response, results_file)

log_message(f"=== GET ALL STUDENTS ===", results_file)
response = requests.get(f"{BASE_URL}/students")
log_result(response, results_file)