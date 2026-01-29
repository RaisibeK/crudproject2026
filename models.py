"""Employee data model definition."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional



@dataclass
class Employee:
    """Employee entity with all required fields."""
    
    first_name: str
    last_name: str
    email: str
    position: str
    salary: float
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Convert employee to dictionary."""
        created_at_str = self.created_at
        if isinstance(self.created_at, datetime):
            created_at_str = self.created_at.isoformat()
        
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "position": self.position,
            "salary": self.salary,
            "created_at": created_at_str,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Employee":
        """Create employee from dictionary."""
        return cls(
            id=data.get("id"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            position=data.get("position"),
            salary=data.get("salary"),
            created_at=data.get("created_at"),
        )
