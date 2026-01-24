"""Employee management service layer - handles all CRUD operations."""

from datetime import datetime
from typing import Dict, List, Optional

from database import db
from models import Employee
from validators import validate_employee_data


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


class NotFoundError(Exception):
    """Raised when employee is not found."""
    pass


class UniqueConstraintError(Exception):
    """Raised when duplicate email is detected."""
    pass


def create_employee(data: dict) -> Employee:
    """
    Create a new employee record.
    
    Args:
        data: Dictionary with employee fields (first_name, last_name, email, position, salary)
        
    Returns:
        Created Employee with id and created_at populated
        
    Raises:
        ValidationError: If data is invalid
        UniqueConstraintError: If email already exists
    """
    # Validate all fields
    is_valid, errors = validate_employee_data(data)
    if not is_valid:
        raise ValidationError(errors)
    
    # Check for duplicate email
    existing = db.execute_single(
        "SELECT id FROM employees WHERE email = ?",
        (data["email"],)
    )
    if existing:
        raise UniqueConstraintError({"email": f"Email '{data['email']}' already exists"})
    
    # Insert new employee
    employee_id = db.execute_insert(
        """
        INSERT INTO employees (first_name, last_name, email, position, salary)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            data["first_name"].strip(),
            data["last_name"].strip(),
            data["email"].strip(),
            data["position"].strip(),
            float(data["salary"]),
        ),
    )
    
    # Fetch and return created employee
    return get_employee_by_id(employee_id)


def get_all_employees(limit: int = 100, offset: int = 0) -> List[Employee]:
    """
    Fetch all employees with pagination.
    
    Args:
        limit: Maximum number of records to return
        offset: Number of records to skip
        
    Returns:
        List of Employee objects
    """
    rows = db.execute_query(
        "SELECT * FROM employees ORDER BY id LIMIT ? OFFSET ?",
        (limit, offset),
    )
    return [Employee.from_dict(row) for row in rows]


def get_employee_by_id(employee_id: int) -> Employee:
    """
    Fetch a single employee by ID.
    
    Args:
        employee_id: Employee ID to fetch
        
    Returns:
        Employee object
        
    Raises:
        NotFoundError: If employee doesn't exist
    """
    row = db.execute_single(
        "SELECT * FROM employees WHERE id = ?",
        (employee_id,),
    )
    
    if not row:
        raise NotFoundError(f"Employee with id {employee_id} not found")
    
    return Employee.from_dict(row)


def update_employee(employee_id: int, data: dict) -> Employee:
    """
    Update employee record with provided fields (partial update allowed).
    
    Args:
        employee_id: ID of employee to update
        data: Dictionary with fields to update
        
    Returns:
        Updated Employee object
        
    Raises:
        NotFoundError: If employee doesn't exist
        ValidationError: If data is invalid
        UniqueConstraintError: If email update causes duplicate
    """
    # Check if employee exists
    existing = get_employee_by_id(employee_id)
    
    # Prepare update data with existing values as defaults
    update_data = {
        "first_name": data.get("first_name", existing.first_name),
        "last_name": data.get("last_name", existing.last_name),
        "email": data.get("email", existing.email),
        "position": data.get("position", existing.position),
        "salary": data.get("salary", existing.salary),
    }
    
    # Validate all fields
    is_valid, errors = validate_employee_data(update_data)
    if not is_valid:
        raise ValidationError(errors)
    
    # Check for duplicate email if email is being updated
    if "email" in data and data["email"] != existing.email:
        duplicate = db.execute_single(
            "SELECT id FROM employees WHERE email = ? AND id != ?",
            (data["email"], employee_id),
        )
        if duplicate:
            raise UniqueConstraintError({"email": f"Email '{data['email']}' already exists"})
    
    # Update only provided fields
    update_fields = []
    update_values = []
    
    if "first_name" in data:
        update_fields.append("first_name = ?")
        update_values.append(data["first_name"].strip())
    if "last_name" in data:
        update_fields.append("last_name = ?")
        update_values.append(data["last_name"].strip())
    if "email" in data:
        update_fields.append("email = ?")
        update_values.append(data["email"].strip())
    if "position" in data:
        update_fields.append("position = ?")
        update_values.append(data["position"].strip())
    if "salary" in data:
        update_fields.append("salary = ?")
        update_values.append(float(data["salary"]))
    
    if update_fields:
        update_values.append(employee_id)
        query = f"UPDATE employees SET {', '.join(update_fields)} WHERE id = ?"
        db.execute_update(query, tuple(update_values))
    
    # Fetch and return updated employee
    return get_employee_by_id(employee_id)


def delete_employee(employee_id: int) -> Dict[str, any]:
    """
    Delete employee by ID.
    
    Args:
        employee_id: ID of employee to delete
        
    Returns:
        Confirmation dict with id and success message
        
    Raises:
        NotFoundError: If employee doesn't exist
    """
    # Check if employee exists
    employee = get_employee_by_id(employee_id)
    
    # Delete employee
    db.execute_delete(
        "DELETE FROM employees WHERE id = ?",
        (employee_id,),
    )
    
    return {
        "id": employee_id,
        "message": f"Employee {employee.first_name} {employee.last_name} deleted successfully",
    }


def get_employee_count() -> int:
    """Get total number of employees."""
    result = db.execute_single("SELECT COUNT(*) as count FROM employees")
    return result["count"] if result else 0
