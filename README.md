# conftest.py

This file sets up shared test fixtures for pytest.
It creates an in-memory SQLite test database, overrides FastAPI’s get_db to use it, and provides a reusable client (for API requests) and db_session (for direct DB access).

This keeps tests isolated, safe, and easy to write.


