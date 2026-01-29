"""Validation functions for employee data."""

import re
from typing import Dict, List, Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email or not isinstance(email, str):
        return False, "Email is required"
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Email format is invalid"
    
    return True, ""


def validate_salary(salary) -> Tuple[bool, str]:
    """
    Validate salary is positive number.
    
    Args:
        salary: Salary value to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        salary_float = float(salary)
        if salary_float <= 0:
            return False, "Salary must be greater than 0"
        return True, ""
    except (TypeError, ValueError):
        return False, "Salary must be a valid number"


def validate_required_field(value, field_name: str) -> Tuple[bool, str]:
    """
    Validate required field is not empty.
    
    Args:
        value: Field value to validate
        field_name: Name of the field for error message
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value or (isinstance(value, str) and not value.strip()):
        return False, f"{field_name} is required"
    return True, ""


def validate_employee_data(data: dict) -> Tuple[bool, Dict[str, str]]:
    """
    Validate all employee fields.
    
    Args:
        data: Dictionary with employee data
        
    Returns:
        Tuple of (is_valid, errors_dict). errors_dict contains field names as keys and error messages as values
    """
    errors = {}
    
    # Validate required fields
    required_fields = {
        "first_name": "First Name",
        "last_name": "Last Name",
        "email": "Email",
        "position": "Position",
        "salary": "Salary",
    }
    
    for field, label in required_fields.items():
        is_valid, error = validate_required_field(data.get(field), label)
        if not is_valid:
            errors[field] = error
    
    # Validate email format if provided
    if "email" in data and data["email"]:
        is_valid, error = validate_email(data["email"])
        if not is_valid:
            errors["email"] = error
    
    # Validate salary if provided
    if "salary" in data and data["salary"] is not None:
        is_valid, error = validate_salary(data["salary"])
        if not is_valid:
            errors["salary"] = error
    
    return len(errors) == 0, errors

