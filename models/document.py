from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List
from enum import Enum

class DocumentStatus(Enum):
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    FINAL = "final"
    ARCHIVED = "archived"

@dataclass
class Document:
    id: str
    name: str
    matter_id: str
    client_name: str
    document_type: str
    current_version: str
    status: str
    tags: List[str]
    extracted_text: str
    key_information: Dict
    created_date: datetime
    last_modified: datetime
    is_privileged: bool
