1. What does Pydantic do?

Pydantic is used for data validation, type enforcement, and serialization in FastAPI.
It ensures that incoming request data matches the expected format and also controls the structure of data returned in responses.

2. Difference between UserCreate and UserResponse

UserCreate defines the data sent from the client to the server (e.g., email and password).
UserResponse defines the data sent from the server to the client (e.g., id, email, created_at).

👉 They are separate to avoid exposing sensitive data like passwords in responses.

3. Why does models.py exist separately from schemas.py?

models.py defines the database structure (tables, columns, relationships) using SQLAlchemy.
schemas.py defines the API structure (input/output validation) using Pydantic.

👉 This separation keeps database logic and API validation clean and independent.

4. What does get_db() do and why does it use yield?

get_db() creates a new database session for each request and ensures it is properly closed after use.

The yield keyword allows FastAPI to:

provide the DB session to the route
pause execution
resume after the request finishes
automatically close the session

👉 This prevents memory leaks and ensures safe DB handling per request.

5. Why do we use .env instead of hardcoding the DB URL?

.env is used to store configuration like database URLs and secrets outside the code.

Benefits:

keeps sensitive data secure
allows easy switching between environments (dev, test, production)
avoids hardcoding credentials in source code
6. What does response_model do in a route?

response_model defines the structure of the response returned to the client.

👉 FastAPI automatically filters the returned data to match this model, ensuring:

only expected fields are sent
sensitive data (like passwords) is excluded
7. One thing I still don’t fully understand

I need more clarity on how FastAPI internally manages dependency injection (like Depends(get_db)) and how request lifecycle works.