from fastapi.testclient import TestClient
from app import app


client = TestClient(app)

def test_create_user():
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "123",
        "user_difficulties": ["ADHD"]
    }
    response = client.post("/users", json=user_data)

    print(f"Response status code: {response.status_code}")
    print(f"Reponse body: {response.text}")
    
    try:
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
        response_json = response.json()
        assert "username" in response_json, 'Response does not contain username field'
        assert response_json["username"] == "testuser", f"Expected username 'testuser', but got '{response_json.get('username')}'"
    except AssertionError as e:
        print(f"Assertion failed: {str(e)}")
        raise

def test_get_user():
    user_id = "66b3a41991b01ecd89eab50b"
    response = client.get(f"/users/{user_id}")
    
    print(f"Response status code: {response.status_code}")
    print(f"Response body: {response.text}")
    
    assert response.status_code == 200
    user = response.json()
    assert user['username'] == "testuser"
    assert user['email'] == "test@example.com"
    assert user['user_difficulties'] == ["ADHD"]

def test_login():
    user_data = {
        "username": "logintest",
        "email": "logintest@example.com",
        "password": "testpassword123",
    }
    create_response = client.post("/users", json=user_data)
    assert create_response.status_code == 200

    login_data = {
        "email": "logintest@example.com",
        "password": "testpassword123",
    }
    login_response = client.post("/login", json=login_data)

    print(f"Login response status code: {login_response.status_code}")
    print(f"Login response body: {login_response.text}")

    assert login_response.status_code == 200
    assert "message" in login_response.json()
    assert login_response.json()["message"] == "Login succesful"
    assert "user_id" in login_response.json()

    incorrect_login_data = {
        "email": "logintest@example.com",
        "password": "wrongPassword",
    }
    incorrect_login_response = client.post("/login", json=incorrect_login_data)
    print(f"Incorrect login response status code: {incorrect_login_response.status_code}")
    assert incorrect_login_response.status_code == 401


if __name__ == "__main__":
    test_login()