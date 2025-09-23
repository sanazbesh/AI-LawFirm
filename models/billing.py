from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict

@dataclass
class TimeEntry:
    id: str
    user_id: str
    matter_id: str
    client_id: str
    date: datetime
    hours: float
    description: str
    billing_rate: float
    billable: bool
    activity_type: str
    status: str
    created_date: datetime

@dataclass
class Invoice:
    id: str
    client_id: str
    matter_id: str
    invoice_number: str
    date_issued: datetime
    due_date: datetime
    line_items: List[Dict]
    subtotal: float
    tax_rate: float
    tax_amount: float
    total_amount: float
    status: str
