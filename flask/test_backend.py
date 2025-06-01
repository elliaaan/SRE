import requests
import random
import string

BASE_URL = "http://34.46.155.201:5000/api"

def random_user():
    name = ''.join(random.choices(string.ascii_letters, k=6))
    email = f"{name.lower()}@mail.ru"
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return {"name": name, "email": email, "password": password}

users = [random_user() for _ in range(3)]
tokens = {}

def test_register_and_login():
    for user in users:
        reg = requests.post(f"{BASE_URL}/auth/register", json=user)
        assert reg.status_code in [200, 400]  # 400 если юзер уже есть
        login = requests.post(f"{BASE_URL}/auth/login", json={
            "email": user["email"],
            "password": user["password"]
        })
        assert login.status_code == 200
        tokens[user["email"]] = login.json()["access_token"]

def test_project_and_task_crud():
    for user in users:
        token = tokens[user["email"]]
        headers = {"Authorization": f"Bearer {token}"}

        # Create project
        proj = requests.post(f"{BASE_URL}/projects", headers=headers, json={"title": f"{user['name']} Project"})
        assert proj.status_code == 200
        project_id = proj.json()["project"]["id"]

        # Get projects
        r = requests.get(f"{BASE_URL}/projects", headers=headers)
        assert r.status_code == 200

        # Update project
        r = requests.put(f"{BASE_URL}/projects/{project_id}", headers=headers, json={"title": "Updated Project"})
        assert r.status_code == 200

        # Create task
        task = requests.post(f"{BASE_URL}/tasks", headers=headers, json={
            "title": f"{user['name']} Task",
            "description": "Important task",
            "project_id": project_id
        })
        assert task.status_code == 201
        task_id = task.json()["task"]["id"]

        # Get tasks
        r = requests.get(f"{BASE_URL}/projects/{project_id}/tasks", headers=headers)
        assert r.status_code == 200

        # Update task
        r = requests.put(f"{BASE_URL}/tasks/{task_id}", headers=headers, json={"title": "Updated Task Title"})
        assert r.status_code == 200

        # Delete task
        r = requests.delete(f"{BASE_URL}/tasks/{task_id}", headers=headers)
        assert r.status_code == 200

        # Delete project
        r = requests.delete(f"{BASE_URL}/projects/{project_id}", headers=headers)
        assert r.status_code == 200
