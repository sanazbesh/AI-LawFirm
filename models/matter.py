from dataclasses import dataclass
from datetime import datetime
from typing import List
from enum import Enum

class MatterType(Enum):
    LITIGATION = "litigation"
    CORPORATE = "corporate"
    FAMILY = "family"
    REAL_ESTATE = "real_estate"
    EMPLOYMENT = "employment"
    INTELLECTUAL_PROPERTY = "intellectual_property"

@dataclass
class Matter:
    id: str
    name: str
    client_id: str
    client_name: str
    matter_type: str
    status: str
    created_date: datetime
    assigned_attorneys: List[str]
    description: str
    budget: float
    estimated_hours: float
    actual_hours: float
