
RUN: python -m pytest -v
# conftest.py

This file sets up the testing environment for the backend. It creates a temporary SQLite database so tests don’t affect real data, resets the database before each test to keep results isolated, and provides a FastAPI TestClient that allows sending fake HTTP requests to the app (like POST or GET) without running a real server.


# test_main.py

This test verifies that the FastAPI backend starts correctly and the /api/health route responds as expected.
It sends a simple GET request using the client fixture from conftest.py, confirming that the API is reachable and the database has initialized without errors.
A successful response (200 OK) with {"status": "ok"} means the backend is fully functional and ready for further endpoint testing.

# test_auth.py

This test file verifies the core authentication logic defined in auth.py.
It checks that user passwords are securely hashed and correctly verified using bcrypt, and that JSON Web Tokens (JWT) are generated, decoded, and expire as expected.
The tests confirm three key security behaviors:
	•	Password hashes never match the plain password and are validated correctly.
	•	Access tokens encode the right user information and can be successfully decoded.
	•	Expired tokens are properly rejected to prevent unauthorized access.
Passing these tests ensures that the authentication system is reliable and secure.


# test_ideas.py 

This test file verifies all main features of the ideas system, including creation, validation, and user interactions.
It checks that only authenticated users can post ideas, validates category rules, ensures public ideas appear in listings, and confirms that users can heart and unheart others’ ideas successfully.
Passing all tests guarantees that the idea creation and sharing mechanics work correctly across all routes


# test_models.py 

This file validates the database structure and relationships between users and ideas.
It checks that each user correctly owns their ideas (one-to-many) and that users can favorite multiple ideas while ideas can belong to multiple users (many-to-many).
Passing these tests ensures the SQLAlchemy models and relationships are properly configured.