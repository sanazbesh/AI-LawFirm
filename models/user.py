from dataclasses import dataclass
from datetime import datetime
from typing import Dict

@dataclass
class User:
    id: str
    email: str
    role: str
    created_date: datetime
    last_login: datetime

@dataclass
class Client:
    id: str
    name: str
    client_type: str
    contact_info: Dict
    created_date: datetime
    status: str
    portal_access: bool
