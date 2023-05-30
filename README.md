# Test task for Go Ahead

To install Python packages:

```
poetry install
```

The task has been solved using Python 3 and PostgreSQL, therefore, to test it PostgreSQL is required <br>
You can provide authentication data in the **.env** file (first create it) following the example from the **.env.example** file <br>

To update database schema:
```
alembic upgrade head
```

To run the FastAPI application:

```
uvicorn main:app --port=8080 
```

Docs for endpoints (by default) can be found at
```
http://localhost:8080/docs
```
