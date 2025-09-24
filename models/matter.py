from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from enum import Enum
import uuid

class MatterType(Enum):
    LITIGATION = "litigation"
    CORPORATE = "corporate"
    FAMILY = "family"
    REAL_ESTATE = "real_estate"
    EMPLOYMENT = "employment"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    TAX = "tax"
    IMMIGRATION = "immigration"
    BANKRUPTCY = "bankruptcy"
    CRIMINAL = "criminal"
    PERSONAL_INJURY = "personal_injury"
    ESTATE_PLANNING = "estate_planning"
    REGULATORY = "regulatory"
    OTHER = "other"

class MatterStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ARCHIVED = "archived"

class Priority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class BillingType(Enum):
    HOURLY = "hourly"
    FIXED_FEE = "fixed_fee"
    CONTINGENCY = "contingency"
    RETAINER = "retainer"
    HYBRID = "hybrid"

@dataclass
class MatterContact:
    name: str
    role: str
    email: str
    phone: str
    is_primary: bool = False
    notes: Optional[str] = None

@dataclass
class MatterDeadline:
    id: str
    description: str
    due_date: datetime
    priority: str = Priority.NORMAL.value
    assigned_to: Optional[str] = None
    is_completed: bool = False
    completed_date: Optional[datetime] = None
    notes: Optional[str] = None
    reminder_dates: List[datetime] = field(default_factory=list)

@dataclass
class MatterTask:
    id: str
    title: str
    description: str
    assigned_to: str
    due_date: Optional[datetime] = None
    priority: str = Priority.NORMAL.value
    status: str = "pending"  # pending, in_progress, completed, cancelled
    created_date: datetime = field(default_factory=datetime.now)
    completed_date: Optional[datetime] = None
    estimated_hours: float = 0.0
    actual_hours: float = 0.0

@dataclass
class MatterNote:
    id: str
    author: str
    content: str
    created_date: datetime
    is_privileged: bool = False
    tags: List[str] = field(default_factory=list)
    attachments: List[str] = field(default_factory=list)

@dataclass
class MatterExpense:
    id: str
    description: str
    amount: float
    date: datetime
    category: str
    is_billable: bool = True
    receipt_path: Optional[str] = None
    status: str = "pending"  # pending, approved, rejected, billed

@dataclass
class CourtInformation:
    court_name: str
    judge_name: Optional[str] = None
    case_number: Optional[str] = None
    filing_date: Optional[datetime] = None
    court_address: Optional[str] = None
    next_hearing_date: Optional[datetime] = None

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
    
    # Enhanced fields
    matter_number: str = ""
    priority: str = Priority.NORMAL.value
    billing_type: str = BillingType.HOURLY.value
    hourly_rate: float = 0.0
    retainer_amount: float = 0.0
    retainer_balance: float = 0.0
    fixed_fee_amount: float = 0.0
    contingency_percentage: float = 0.0
    
    # Dates and timeline
    opened_date: Optional[datetime] = None
    closed_date: Optional[datetime] = None
    statute_of_limitations: Optional[datetime] = None
    expected_completion_date: Optional[datetime] = None
    
    # Financial tracking
    total_billed: float = 0.0
    total_collected: float = 0.0
    total_expenses: float = 0.0
    write_offs: float = 0.0
    
    # Relationships and contacts
    contacts: List[MatterContact] = field(default_factory=list)
    opposing_parties: List[str] = field(default_factory=list)
    opposing_counsel: List[str] = field(default_factory=list)
    
    # Tasks and deadlines
    deadlines: List[MatterDeadline] = field(default_factory=list)
    tasks: List[MatterTask] = field(default_factory=list)
    
    # Documentation and notes
    notes: List[MatterNote] = field(default_factory=list)
    document_ids: List[str] = field(default_factory=list)
    
    # Court information (for litigation matters)
    court_info: Optional[CourtInformation] = None
    
    # Expenses and costs
    expenses: List[MatterExpense] = field(default_factory=list)
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    
    # Tracking
    created_by: str = ""
    last_modified: datetime = field(default_factory=datetime.now)
    last_modified_by: str = ""
    
    def __post_init__(self):
        """Post-initialization processing."""
        if not self.matter_number:
            self.matter_number = self.generate_matter_number()
        if not self.opened_date:
            self.opened_date = self.created_date

    @property
    def is_active(self) -> bool:
        """Check if the matter is currently active."""
        return self.status == MatterStatus.ACTIVE.value
    
    @property
    def is_billable(self) -> bool:
        """Check if the matter allows billing."""
        return self.billing_type != "no_charge" and self.status not in [MatterStatus.CANCELLED.value, MatterStatus.ARCHIVED.value]
    
    @property
    def days_open(self) -> int:
        """Calculate number of days the matter has been open."""
        if self.closed_date:
            return (self.closed_date - self.opened_date).days
        return (datetime.now() - self.opened_date).days if self.opened_date else 0
    
    @property
    def hours_variance(self) -> float:
        """Calculate variance between estimated and actual hours."""
        return self.actual_hours - self.estimated_hours
    
    @property
    def budget_variance(self) -> float:
        """Calculate variance between budget and actual billing."""
        return self.total_billed - self.budget
    
    @property
    def budget_utilization(self) -> float:
        """Calculate percentage of budget utilized."""
        if self.budget == 0:
            return 0.0
        return (self.total_billed / self.budget) * 100
    
    @property
    def collection_rate(self) -> float:
        """Calculate collection rate percentage."""
        if self.total_billed == 0:
            return 0.0
        return (self.total_collected / self.total_billed) * 100
    
    @property
    def profitability(self) -> float:
        """Calculate matter profitability."""
        return self.total_collected - self.total_expenses - self.write_offs
    
    @property
    def pending_deadlines(self) -> List[MatterDeadline]:
        """Get all pending deadlines."""
        return [d for d in self.deadlines if not d.is_completed and d.due_date >= datetime.now()]
    
    @property
    def overdue_deadlines(self) -> List[MatterDeadline]:
        """Get all overdue deadlines."""
        return [d for d in self.deadlines if not d.is_completed and d.due_date < datetime.now()]
    
    @property
    def upcoming_deadlines(self, days: int = 7) -> List[MatterDeadline]:
        """Get deadlines due within specified number of days."""
        future_date = datetime.now() + timedelta(days=days)
        return [d for d in self.deadlines if not d.is_completed and datetime.now() <= d.due_date <= future_date]
    
    @property
    def open_tasks(self) -> List[MatterTask]:
        """Get all open tasks."""
        return [t for t in self.tasks if t.status not in ["completed", "cancelled"]]
    
    @property
    def overdue_tasks(self) -> List[MatterTask]:
        """Get all overdue tasks."""
        return [t for t in self.tasks if t.due_date and t.due_date < datetime.now() and t.status not in ["completed", "cancelled"]]
    
    def generate_matter_number(self) -> str:
        """Generate a unique matter number."""
        year = self.created_date.year
        # Simple format: YYYY-MMMM (year + 4-digit sequential)
        # In a real implementation, this would query the database for the next number
        return f"{year}-{str(uuid.uuid4())[:4].upper()}"
    
    def add_attorney(self, attorney_id: str) -> None:
        """Add an attorney to the matter."""
        if attorney_id not in self.assigned_attorneys:
            self.assigned_attorneys.append(attorney_id)
            self.last_modified = datetime.now()
    
    def remove_attorney(self, attorney_id: str) -> None:
        """Remove an attorney from the matter."""
        if attorney_id in self.assigned_attorneys:
            self.assigned_attorneys.remove(attorney_id)
            self.last_modified = datetime.now()
    
    def add_contact(self, name: str, role: str, email: str, phone: str, 
                   is_primary: bool = False, notes: str = None) -> MatterContact:
        """Add a contact to the matter."""
        # If setting as primary, unset other primary contacts
        if is_primary:
            for contact in self.contacts:
                contact.is_primary = False
        
        contact = MatterContact(
            name=name,
            role=role,
            email=email,
            phone=phone,
            is_primary=is_primary,
            notes=notes
        )
        
        self.contacts.append(contact)
        self.last_modified = datetime.now()
        return contact
    
    def add_deadline(self, description: str, due_date: datetime, 
                    priority: str = Priority.NORMAL.value, assigned_to: str = None,
                    reminder_dates: List[datetime] = None) -> MatterDeadline:
        """Add a deadline to the matter."""
        deadline = MatterDeadline(
            id=str(uuid.uuid4()),
            description=description,
            due_date=due_date,
            priority=priority,
            assigned_to=assigned_to,
            reminder_dates=reminder_dates or []
        )
        
        self.deadlines.append(deadline)
        self.last_modified = datetime.now()
        return deadline
    
    def complete_deadline(self, deadline_id: str, completed_by: str, notes: str = None) -> bool:
        """Mark a deadline as completed."""
        for deadline in self.deadlines:
            if deadline.id == deadline_id:
                deadline.is_completed = True
                deadline.completed_date = datetime.now()
                if notes:
                    deadline.notes = notes
                self.last_modified = datetime.now()
                return True
        return False
    
    def add_task(self, title: str, description: str, assigned_to: str,
                due_date: datetime = None, priority: str = Priority.NORMAL.value,
                estimated_hours: float = 0.0) -> MatterTask:
        """Add a task to the matter."""
        task = MatterTask(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            assigned_to=assigned_to,
            due_date=due_date,
            priority=priority,
            estimated_hours=estimated_hours
        )
        
        self.tasks.append(task)
        self.last_modified = datetime.now()
        return task
    
    def complete_task(self, task_id: str, actual_hours: float = 0.0) -> bool:
        """Mark a task as completed."""
        for task in self.tasks:
            if task.id == task_id:
                task.status = "completed"
                task.completed_date = datetime.now()
                task.actual_hours = actual_hours
                self.last_modified = datetime.now()
                return True
        return False
    
    def add_note(self, author: str, content: str, is_privileged: bool = False,
                tags: List[str] = None, attachments: List[str] = None) -> MatterNote:
        """Add a note to the matter."""
        note = MatterNote(
            id=str(uuid.uuid4()),
            author=author,
            content=content,
            created_date=datetime.now(),
            is_privileged=is_privileged,
            tags=tags or [],
            attachments=attachments or []
        )
        
        self.notes.append(note)
        self.last_modified = datetime.now()
        return note
    
    def add_expense(self, description: str, amount: float, date: datetime,
                   category: str, is_billable: bool = True, receipt_path: str = None) -> MatterExpense:
        """Add an expense to the matter."""
        expense = MatterExpense(
            id=str(uuid.uuid4()),
            description=description,
            amount=amount,
            date=date,
            category=category,
            is_billable=is_billable,
            receipt_path=receipt_path
        )
        
        self.expenses.append(expense)
        self.total_expenses += amount
        self.last_modified = datetime.now()
        return expense
    
    def update_financial_totals(self, billed_amount: float = None, collected_amount: float = None,
                               expense_amount: float = None, write_off_amount: float = None) -> None:
        """Update financial totals."""
        if billed_amount is not None:
            self.total_billed += billed_amount
        if collected_amount is not None:
            self.total_collected += collected_amount
        if expense_amount is not None:
            self.total_expenses += expense_amount
        if write_off_amount is not None:
            self.write_offs += write_off_amount
        
        self.last_modified = datetime.now()
    
    def update_time_tracking(self, hours: float) -> None:
        """Update actual hours worked."""
        self.actual_hours += hours
        self.last_modified = datetime.now()
    
    def set_court_information(self, court_name: str, judge_name: str = None,
                             case_number: str = None, filing_date: datetime = None,
                             court_address: str = None, next_hearing_date: datetime = None) -> None:
        """Set court information for litigation matters."""
        self.court_info = CourtInformation(
            court_name=court_name,
            judge_name=judge_name,
            case_number=case_number,
            filing_date=filing_date,
            court_address=court_address,
            next_hearing_date=next_hearing_date
        )
        self.last_modified = datetime.now()
    
    def close_matter(self, closed_by: str, closing_notes: str = None) -> None:
        """Close the matter."""
        self.status = MatterStatus.COMPLETED.value
        self.closed_date = datetime.now()
        self.last_modified = datetime.now()
        self.last_modified_by = closed_by
        
        if closing_notes:
            self.add_note(closed_by, f"Matter closed: {closing_notes}")
    
    def archive_matter(self, archived_by: str) -> None:
        """Archive the matter."""
        self.status = MatterStatus.ARCHIVED.value
        self.last_modified = datetime.now()
        self.last_modified_by = archived_by
    
    def get_matter_summary(self) -> Dict[str, Any]:
        """Get a summary of the matter."""
        return {
            "id": self.id,
            "name": self.name,
            "matter_number": self.matter_number,
            "client_name": self.client_name,
            "matter_type": self.matter_type,
            "status": self.status,
            "priority": self.priority,
            "days_open": self.days_open,
            "assigned_attorneys": len(self.assigned_attorneys),
            "budget": self.budget,
            "budget_utilization": round(self.budget_utilization, 2),
            "estimated_hours": self.estimated_hours,
            "actual_hours": self.actual_hours,
            "hours_variance": self.hours_variance,
            "total_billed": self.total_billed,
            "total_collected": self.total_collected,
            "collection_rate": round(self.collection_rate, 2),
            "profitability": self.profitability,
            "open_tasks": len(self.open_tasks),
            "overdue_tasks": len(self.overdue_tasks),
            "pending_deadlines": len(self.pending_deadlines),
            "overdue_deadlines": len(self.overdue_deadlines),
            "total_notes": len(self.notes),
            "total_expenses": self.total_expenses,
            "created_date": self.created_date,
            "last_modified": self.last_modified
        }

@dataclass
class MatterSearchCriteria:
    """Criteria for searching matters."""
    text_query: Optional[str] = None
    matter_types: List[str] = field(default_factory=list)
    statuses: List[str] = field(default_factory=list)
    priorities: List[str] = field(default_factory=list)
    client_ids: List[str] = field(default_factory=list)
    assigned_attorneys: List[str] = field(default_factory=list)
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
    opened_after: Optional[datetime] = None
    opened_before: Optional[datetime] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    has_overdue_deadlines: Optional[bool] = None
    has_overdue_tasks: Optional[bool] = None
    billing_types: List[str] = field(default_factory=list)

class MatterManager:
    """Utility class for matter operations."""
    
    @staticmethod
    def create_matter(name: str, client_id: str, client_name: str, matter_type: str,
                     created_by: str, description: str = "", budget: float = 0.0,
                     estimated_hours: float = 0.0) -> Matter:
        """Create a new matter with default values."""
        matter_id = str(uuid.uuid4())
        current_time = datetime.now()
        
        matter = Matter(
            id=matter_id,
            name=name,
            client_id=client_id,
            client_name=client_name,
            matter_type=matter_type,
            status=MatterStatus.ACTIVE.value,
            created_date=current_time,
            assigned_attorneys=[],
            description=description,
            budget=budget,
            estimated_hours=estimated_hours,
            actual_hours=0.0,
            created_by=created_by,
            last_modified_by=created_by
        )
        
        return matter
    
    @staticmethod
    def filter_matters(matters: List[Matter], criteria: MatterSearchCriteria) -> List[Matter]:
        """Filter matters based on search criteria."""
        filtered = matters
        
        if criteria.text_query:
            query_lower = criteria.text_query.lower()
            filtered = [
                matter for matter in filtered
                if query_lower in matter.name.lower() or
                   query_lower in matter.description.lower() or
                   query_lower in matter.matter_number.lower() or
                   any(query_lower in tag.lower() for tag in matter.tags)
            ]
        
        if criteria.matter_types:
            filtered = [matter for matter in filtered if matter.matter_type in criteria.matter_types]
        
        if criteria.statuses:
            filtered = [matter for matter in filtered if matter.status in criteria.statuses]
        
        if criteria.priorities:
            filtered = [matter for matter in filtered if matter.priority in criteria.priorities]
        
        if criteria.client_ids:
            filtered = [matter for matter in filtered if matter.client_id in criteria.client_ids]
        
        if criteria.assigned_attorneys:
            filtered = [
                matter for matter in filtered
                if any(attorney in matter.assigned_attorneys for attorney in criteria.assigned_attorneys)
            ]
        
        if criteria.created_after:
            filtered = [matter for matter in filtered if matter.created_date >= criteria.created_after]
        
        if criteria.created_before:
            filtered = [matter for matter in filtered if matter.created_date <= criteria.created_before]
        
        if criteria.budget_min is not None:
            filtered = [matter for matter in filtered if matter.budget >= criteria.budget_min]
        
        if criteria.budget_max is not None:
            filtered = [matter for matter in filtered if matter.budget <= criteria.budget_max]
        
        if criteria.has_overdue_deadlines is not None:
            filtered = [
                matter for matter in filtered
                if bool(matter.overdue_deadlines) == criteria.has_overdue_deadlines
            ]
        
        if criteria.has_overdue_tasks is not None:
            filtered = [
                matter for matter in filtered
                if bool(matter.overdue_tasks) == criteria.has_overdue_tasks
            ]
        
        if criteria.billing_types:
            filtered = [matter for matter in filtered if matter.billing_type in criteria.billing_types]
        
        return filtered
    
    @staticmethod
    def get_matter_statistics(matters: List[Matter]) -> Dict[str, Any]:
        """Generate statistics for a collection of matters."""
        if not matters:
            return {}
        
        total_matters = len(matters)
        active_matters = len([m for m in matters if m.is_active])
        
        # Status distribution
        status_counts = {}
        for matter in matters:
            status_counts[matter.status] = status_counts.get(matter.status, 0) + 1
        
        # Type distribution
        type_counts = {}
        for matter in matters:
            type_counts[matter.matter_type] = type_counts.get(matter.matter_type, 0) + 1
        
        # Financial totals
        total_budget = sum(matter.budget for matter in matters)
        total_billed = sum(matter.total_billed for matter in matters)
        total_collected = sum(matter.total_collected for matter in matters)
        
        return {
            "total_matters": total_matters,
            "active_matters": active_matters,
            "status_distribution": status_counts,
            "type_distribution": type_counts,
            "total_budget": total_budget,
            "total_billed": total_billed,
            "total_collected": total_collected,
            "average_budget": total_budget / total_matters if total_matters > 0 else 0,
            "overall_collection_rate": (total_collected / total_billed * 100) if total_billed > 0 else 0,
            "matters_with_overdue_deadlines": len([m for m in matters if m.overdue_deadlines]),
            "matters_with_overdue_tasks": len([m for m in matters if m.overdue_tasks]),
            "average_days_open": sum(m.days_open for m in matters) / total_matters if total_matters > 0 else 0
        }
