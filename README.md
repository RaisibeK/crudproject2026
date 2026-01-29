# Employee Management System - CRUD Application

A Python-based employee management system using Flask and SQLite3. This application allows you to create, read, update, and delete employee records with full validation and error handling.

## Features

- ✅ **Create** employees with validation (unique emails, positive salary)
- ✅ **Read** all employees with pagination support
- ✅ **Read** single employee by ID
- ✅ **Update** employee records (partial updates supported)
- ✅ **Delete** employees with confirmation
- ✅ SQLite3 database (no ORM dependency)
- ✅ Full input validation (email format, required fields, positive salary)
- ✅ RESTful API endpoints
- ✅ Proper error handling with meaningful responses

## Technology Stack

- **Language**: Python 3.7+
- **Framework**: Flask 2.3.3
- **Database**: SQLite3 (built-in)
- **No ORM**: Direct SQL with sqlite3 module

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory**:
   ```bash
   cd crudproject2026
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

   The application will start at `http://localhost:5000`

## Database

The application automatically creates a SQLite database file `employees.db` in the project directory on first run. The database schema includes:

```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    position TEXT NOT NULL,
    salary REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## API Endpoints

### 1. Create Employee
**POST** `/employees`

Request body:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "position": "Software Engineer",
  "salary": 75000
}
```

Response (201 Created):
```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "position": "Software Engineer",
  "salary": 75000,
  "created_at": "2026-01-21T10:30:00"
}
```

### 2. Get All Employees
**GET** `/employees?limit=100&offset=0`

Query parameters:
- `limit` (optional): Number of records to return (default: 100)
- `offset` (optional): Number of records to skip (default: 0)

Response (200 OK):
```json
{
  "employees": [
    {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com",
      "position": "Software Engineer",
      "salary": 75000,
      "created_at": "2026-01-21T10:30:00"
    }
  ],
  "count": 1
}
```

### 3. Get Single Employee
**GET** `/employees/{id}`

Response (200 OK):
```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "position": "Software Engineer",
  "salary": 75000,
  "created_at": "2026-01-21T10:30:00"
}
```

### 4. Update Employee
**PUT** `/employees/{id}`

Request body (partial update - only include fields to change):
```json
{
  "position": "Senior Software Engineer",
  "salary": 95000
}
```

Response (200 OK): Updated employee object

### 5. Delete Employee
**DELETE** `/employees/{id}`

Response (200 OK):
```json
{
  "id": 1,
  "message": "Employee John Doe deleted successfully"
}
```

## Validation Rules

- **Email**: Must be valid email format and unique across all employees
- **Salary**: Must be a positive number (> 0)
- **Required Fields**: first_name, last_name, email, position, salary
- **No empty strings**: All string fields are trimmed

## Error Responses

### 400 Bad Request - Validation Error
```json
{
  "errors": {
    "email": "Email format is invalid",
    "salary": "Salary must be greater than 0"
  }
}
```

### 404 Not Found
```json
{
  "error": "Employee with id 999 not found"
}
```

### 409 Conflict - Duplicate Email
```json
{
  "errors": {
    "email": "Email 'john.doe@example.com' already exists"
  }
}
```

## Example Usage with curl

```bash
# Create employee
curl -X POST http://localhost:5000/employees \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Jane","last_name":"Smith","email":"jane@example.com","position":"Product Manager","salary":85000}'

# Get all employees
curl http://localhost:5000/employees

# Get single employee
curl http://localhost:5000/employees/1

# Update employee
curl -X PUT http://localhost:5000/employees/1 \
  -H "Content-Type: application/json" \
  -d '{"salary":90000}'

# Delete employee
curl -X DELETE http://localhost:5000/employees/1

# Health check
curl http://localhost:5000/health
```

## Project Structure

```
crudproject2026/
├── app.py                 # Flask application with API routes
├── models.py              # Employee dataclass definition
├── database.py            # SQLite connection and initialization
├── validators.py          # Input validation functions
├── employees_manager.py   # Service layer with CRUD operations
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── employees.db          # SQLite database (auto-created)
```

## Scaling Considerations (100k+ Employees)

For production deployment with 100,000+ employees:

1. **Database Optimization**:
   - Add indexes on `email` (unique), `created_at`, and frequently queried fields
   - Consider partitioning by `created_at` for archival

2. **Query Optimization**:
   - Implement pagination with cursor-based pagination (faster than offset)
   - Use connection pooling (e.g., pgbouncer for PostgreSQL if migrating)

3. **Infrastructure**:
   - Migrate from SQLite to PostgreSQL or similar for concurrent writes
   - Deploy with production WSGI server (Gunicorn, uWSGI)
   - Add caching layer (Redis) for frequently accessed employees

4. **API Design**:
   - Implement rate limiting
   - Add bulk operation endpoints (batch create/update)
   - Support filtering and sorting parameters

5. **Data Management**:
   - Archive old/deleted records to separate tables
   - Implement soft deletes instead of hard deletes

## Testing

No test suite included in this project. To add tests, consider:

```bash
pip install pytest
pytest tests/
```

## Notes

- Database file `employees.db` is auto-created on first run
- Add `employees.db` to `.gitignore` to avoid committing local database
- In debug mode, the app reloads on file changes
- For production, set `debug=False` and use a production WSGI server

## License

This is an internship assessment project.

