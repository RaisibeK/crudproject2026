# Copilot Instructions for crudproject2026

## Project Overview
**Employee Management System** - A Python CRUD application for managing employee records. Scope: Create, read, update, and delete employee records with validation and proper error handling. This is an internship assessment project focusing on Python fundamentals, database interaction, and clean application structure.

## Employee Entity
```python
id          # integer, auto-generated (Primary Key)
first_name  # string, required
last_name   # string, required
email       # string, required, unique constraint
position    # string, required
salary      # decimal/float, required (must be positive)
created_at  # datetime, auto-generated (server timestamp)
```

## Architecture & Key Components

### Required Structure
```
crudproject2026/
├── app.py                 # Main entry point (routes/CLI commands)
├── models.py              # Employee model definition
├── database.py            # Database connection & initialization
├── validators.py          # Validation logic
├── employees_manager.py   # Service layer (CRUD operations)
├── requirements.txt       # Dependencies
└── README.md             # Setup & usage instructions
```

### Layered Architecture Pattern
1. **Models layer** (`models.py`) - Define Employee data structure (SQLAlchemy or dataclass)
2. **Database layer** (`database.py`) - Connection, session management, initialization
3. **Service/Business layer** (`employees_manager.py`) - CRUD logic, no HTTP awareness
4. **Validation layer** (`validators.py`) - Email format, salary positivity, required fields
5. **Route/Controller layer** (`app.py`) - Flask/FastAPI routes OR CLI commands

## CRUD Operations Implementation

### CREATE - Add Employee
- Validate required fields (all 5: first_name, last_name, email, position, salary)
- Validate email format using regex or email_validator library
- Validate salary is positive (> 0)
- Check for duplicate email before insert
- Auto-generate id and created_at on insert
- Return created employee with id, or raise ValidationError with specific field errors
- **Location**: `employees_manager.py::create_employee(data: dict) -> Employee`

### READ - Fetch Employees
- **Get all**: Return list of all employees with pagination support (future-proof)
- **Get single by ID**: Return employee if exists, raise NotFoundError if id doesn't match
- Both return Employee objects serialized to dict/JSON
- **Locations**: `employees_manager.py::get_all_employees()`, `employees_manager.py::get_employee_by_id(id: int)`

### UPDATE - Modify Employee
- Accept only provided fields (partial update allowed)
- Re-validate email uniqueness if email field is updated
- Re-validate salary if provided
- Raise NotFoundError for invalid IDs
- Return updated employee record
- **Location**: `employees_manager.py::update_employee(id: int, data: dict) -> Employee`

### DELETE - Remove Employee
- Find employee by ID, raise NotFoundError if not exists
- Delete and return confirmation (id + success message)
- **Location**: `employees_manager.py::delete_employee(id: int) -> dict`

## API Endpoints (Web Framework)
If using Flask/FastAPI implement these:
```
POST   /employees       – Create new employee (body: JSON with all 5 fields)
GET    /employees       – List all employees (optional: ?page=1&limit=10)
GET    /employees/{id}  – Get single employee by ID
PUT    /employees/{id}  – Update employee (body: JSON with fields to update)
DELETE /employees/{id}  – Delete employee
```

## Validation Rules
All validation in `validators.py`:
- **Email**: Valid format (use regex pattern or `email_validator` library), must be unique in database
- **Salary**: Must be numeric, > 0 (reject 0 or negative)
- **Required fields**: first_name, last_name, email, position, salary - no empty strings
- **Response format**: Return errors as `{"field": "error message"}` dict for batch validation feedback

## Error Handling Pattern
- **ValidationError** - Invalid data (wrong format, negative salary, missing fields)
- **UniqueConstraintError** - Duplicate email detected
- **NotFoundError** - Employee ID doesn't exist
- **DatabaseError** - Connection/transaction failures
Return appropriate HTTP status codes (400 for validation, 404 for not found, 500 for server errors)

## Development Patterns

### Code Style
- Use Python type hints throughout (e.g., `def create_employee(data: dict) -> Employee:`)
- Separate concerns: models ≠ routes ≠ validation ≠ database queries
- Follow PEP 8; use meaningful variable names

### Database Choice & Setup
- **Recommended**: SQLite with SQLAlchemy ORM for simplicity
- Connection string: Store in `.env` or environment variable (use `python-dotenv`)
- Database file: `crudproject2026/employees.db` (add to .gitignore)
- Initialize schema on first run if DB doesn't exist

### Code Structure Example
```python
# models.py - Define Employee using SQLAlchemy
class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    # ... other fields

# validators.py - Standalone validation functions
def validate_email(email: str) -> bool
def validate_salary(salary: float) -> bool

# employees_manager.py - Service layer, no DB session handling
def create_employee(data: dict) -> Employee:
    # validate, check duplicates, then delegate to database layer
    
# app.py - Routes only (Flask/FastAPI or CLI)
@app.post("/employees")
def create_employee_endpoint(data: dict):
    # call service layer, handle exceptions, return response
```

## Testing & Execution
- **Run CLI version**: `python -m crudproject2026.app` (if CLI)
- **Run Flask/FastAPI**: `python crudproject2026/app.py` (with `if __name__ == "__main__"` entry point)
- **Database init**: Script or auto-init on first app run
- No test suite required for this assessment, but consider `pytest` structure for code quality impression

## Important Notes
- **Scale consideration** (stretch question): For 100k+ employees, consider:
  - Database indexing on email and frequently searched fields
  - Pagination (offset-limit or cursor-based) for list endpoints
  - Connection pooling if using SQLAlchemy
  - Potential data archival strategy for deleted records
- `.git` initialized - commit messages should describe CRUD operations (e.g., "feat: add employee create endpoint")
- Add `.gitignore` entry: `*.db`, `.env`, `__pycache__/`, `*.pyc`

## Deliverables Checklist
- [ ] Source code with all CRUD operations
- [ ] README.md with setup instructions (how to install, run, use the app)
- [ ] requirements.txt with all dependencies
- [ ] Example curl/Postman requests OR CLI usage examples
- [ ] Clean git history with meaningful commit messages


