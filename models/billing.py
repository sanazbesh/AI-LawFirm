from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum
import uuid

class TimeEntryStatus(Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    BILLED = "billed"
    REJECTED = "rejected"

class InvoiceStatus(Enum):
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    PARTIAL = "partial"

class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class ActivityType(Enum):
    LEGAL_RESEARCH = "Legal Research"
    DOCUMENT_REVIEW = "Document Review"
    CLIENT_MEETING = "Client Meeting"
    COURT_APPEARANCE = "Court Appearance"
    DRAFTING = "Drafting"
    PHONE_CONFERENCE = "Phone Conference"
    EMAIL_COMMUNICATION = "Email Communication"
    CASE_PREPARATION = "Case Preparation"
    ADMINISTRATIVE = "Administrative"
    TRAVEL = "Travel"
    DEPOSITION = "Deposition"
    NEGOTIATION = "Negotiation"

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
    modified_date: Optional[datetime] = None
    approved_by: Optional[str] = None
    approved_date: Optional[datetime] = None
    notes: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    
    @property
    def total_amount(self) -> float:
        """Calculate the total billable amount for this time entry."""
        return self.hours * self.billing_rate if self.billable else 0.0
    
    def approve(self, approved_by: str) -> None:
        """Approve this time entry."""
        self.status = TimeEntryStatus.APPROVED.value
        self.approved_by = approved_by
        self.approved_date = datetime.now()
        self.modified_date = datetime.now()
    
    def reject(self, notes: str = None) -> None:
        """Reject this time entry."""
        self.status = TimeEntryStatus.REJECTED.value
        if notes:
            self.notes = notes
        self.modified_date = datetime.now()

@dataclass
class ExpenseEntry:
    id: str
    user_id: str
    matter_id: str
    client_id: str
    date: datetime
    amount: float
    description: str
    category: str
    billable: bool
    receipt_attached: bool
    status: str
    created_date: datetime
    modified_date: Optional[datetime] = None
    approved_by: Optional[str] = None
    approved_date: Optional[datetime] = None
    
    @property
    def billable_amount(self) -> float:
        """Return the billable amount for this expense."""
        return self.amount if self.billable else 0.0

@dataclass
class InvoiceLineItem:
    description: str
    quantity: float
    rate: float
    amount: float
    date_range: Optional[str] = None
    matter_reference: Optional[str] = None
    
    @classmethod
    def from_time_entry(cls, time_entry: TimeEntry) -> 'InvoiceLineItem':
        """Create an invoice line item from a time entry."""
        return cls(
            description=f"{time_entry.activity_type}: {time_entry.description}",
            quantity=time_entry.hours,
            rate=time_entry.billing_rate,
            amount=time_entry.total_amount,
            date_range=time_entry.date.strftime("%Y-%m-%d")
        )
    
    @classmethod
    def from_expense_entry(cls, expense_entry: ExpenseEntry) -> 'InvoiceLineItem':
        """Create an invoice line item from an expense entry."""
        return cls(
            description=f"Expense: {expense_entry.description}",
            quantity=1.0,
            rate=expense_entry.amount,
            amount=expense_entry.billable_amount,
            date_range=expense_entry.date.strftime("%Y-%m-%d")
        )

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
    created_date: Optional[datetime] = None
    sent_date: Optional[datetime] = None
    paid_date: Optional[datetime] = None
    payment_terms: str = "Net 30"
    notes: Optional[str] = None
    discount_amount: float = 0.0
    discount_percentage: float = 0.0
    
    def __post_init__(self):
        if self.created_date is None:
            self.created_date = datetime.now()
    
    @property
    def is_overdue(self) -> bool:
        """Check if the invoice is overdue."""
        return datetime.now() > self.due_date and self.status not in [InvoiceStatus.PAID.value, InvoiceStatus.CANCELLED.value]
    
    @property
    def days_overdue(self) -> int:
        """Calculate how many days overdue the invoice is."""
        if not self.is_overdue:
            return 0
        return (datetime.now() - self.due_date).days
    
    @property
    def amount_due(self) -> float:
        """Calculate the amount still due on this invoice."""
        if self.status == InvoiceStatus.PAID.value:
            return 0.0
        return self.total_amount
    
    def mark_as_sent(self) -> None:
        """Mark the invoice as sent."""
        self.status = InvoiceStatus.SENT.value
        self.sent_date = datetime.now()
    
    def mark_as_paid(self, payment_date: datetime = None) -> None:
        """Mark the invoice as paid."""
        self.status = InvoiceStatus.PAID.value
        self.paid_date = payment_date or datetime.now()
    
    def calculate_totals(self) -> None:
        """Recalculate invoice totals based on line items."""
        self.subtotal = sum(item.get('amount', 0) for item in self.line_items)
        
        # Apply discount
        if self.discount_percentage > 0:
            self.discount_amount = self.subtotal * (self.discount_percentage / 100)
        
        discounted_subtotal = self.subtotal - self.discount_amount
        self.tax_amount = discounted_subtotal * self.tax_rate
        self.total_amount = discounted_subtotal + self.tax_amount

@dataclass
class Payment:
    id: str
    invoice_id: str
    amount: float
    payment_date: datetime
    payment_method: str
    reference_number: Optional[str] = None
    status: str = PaymentStatus.COMPLETED.value
    notes: Optional[str] = None
    created_date: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_date is None:
            self.created_date = datetime.now()

@dataclass
class BillingRate:
    id: str
    user_id: str
    matter_id: Optional[str] = None
    client_id: Optional[str] = None
    activity_type: Optional[str] = None
    rate: float = 0.0
    effective_date: datetime = field(default_factory=datetime.now)
    end_date: Optional[datetime] = None
    is_active: bool = True
    
    def is_applicable(self, user_id: str, matter_id: str = None, 
                     client_id: str = None, activity_type: str = None,
                     date: datetime = None) -> bool:
        """Check if this billing rate applies to the given criteria."""
        check_date = date or datetime.now()
        
        # Check if rate is active and within date range
        if not self.is_active:
            return False
        if check_date < self.effective_date:
            return False
        if self.end_date and check_date > self.end_date:
            return False
        
        # Check user match
        if self.user_id != user_id:
            return False
        
        # Check specific criteria (more specific rates take precedence)
        if self.matter_id and self.matter_id != matter_id:
            return False
        if self.client_id and self.client_id != client_id:
            return False
        if self.activity_type and self.activity_type != activity_type:
            return False
        
        return True

@dataclass
class BillingSummary:
    """Summary of billing information for reporting purposes."""
    period_start: datetime
    period_end: datetime
    total_hours: float = 0.0
    billable_hours: float = 0.0
    non_billable_hours: float = 0.0
    total_revenue: float = 0.0
    total_expenses: float = 0.0
    invoices_sent: int = 0
    invoices_paid: int = 0
    outstanding_amount: float = 0.0
    collection_rate: float = 0.0
    
    @property
    def billable_percentage(self) -> float:
        """Calculate the percentage of billable hours."""
        if self.total_hours == 0:
            return 0.0
        return (self.billable_hours / self.total_hours) * 100
    
    @property
    def average_hourly_rate(self) -> float:
        """Calculate the average hourly billing rate."""
        if self.billable_hours == 0:
            return 0.0
        return self.total_revenue / self.billable_hours

class BillingCalculator:
    """Utility class for billing calculations."""
    
    @staticmethod
    def calculate_invoice_totals(line_items: List[Dict], tax_rate: float = 0.0,
                               discount_percentage: float = 0.0) -> Dict[str, float]:
        """Calculate invoice totals from line items."""
        subtotal = sum(item.get('amount', 0) for item in line_items)
        discount_amount = subtotal * (discount_percentage / 100)
        discounted_subtotal = subtotal - discount_amount
        tax_amount = discounted_subtotal * tax_rate
        total = discounted_subtotal + tax_amount
        
        return {
            'subtotal': subtotal,
            'discount_amount': discount_amount,
            'tax_amount': tax_amount,
            'total_amount': total
        }
    
    @staticmethod
    def get_applicable_rate(rates: List[BillingRate], user_id: str,
                          matter_id: str = None, client_id: str = None,
                          activity_type: str = None, date: datetime = None) -> float:
        """Find the most applicable billing rate from a list of rates."""
        applicable_rates = [
            rate for rate in rates
            if rate.is_applicable(user_id, matter_id, client_id, activity_type, date)
        ]
        
        if not applicable_rates:
            return 0.0
        
        # Sort by specificity (more specific rates first)
        def rate_specificity(rate: BillingRate) -> int:
            specificity = 0
            if rate.matter_id:
                specificity += 4
            if rate.client_id:
                specificity += 2
            if rate.activity_type:
                specificity += 1
            return specificity
        
        applicable_rates.sort(key=rate_specificity, reverse=True)
        return applicable_rates[0].rate
    
    @staticmethod
    def generate_invoice_number(prefix: str = "INV", date: datetime = None) -> str:
        """Generate a unique invoice number."""
        invoice_date = date or datetime.now()
        timestamp = invoice_date.strftime("%Y%m%d")
        random_suffix = str(uuid.uuid4())[:8].upper()
        return f"{prefix}-{timestamp}-{random_suffix}"
    
    @staticmethod
    def calculate_aging(invoices: List[Invoice]) -> Dict[str, float]:
        """Calculate aging report for outstanding invoices."""
        aging = {
            'current': 0.0,
            '1-30_days': 0.0,
            '31-60_days': 0.0,
            '61-90_days': 0.0,
            'over_90_days': 0.0
        }
        
        current_date = datetime.now()
        
        for invoice in invoices:
            if invoice.status in [InvoiceStatus.PAID.value, InvoiceStatus.CANCELLED.value]:
                continue
            
            days_overdue = (current_date - invoice.due_date).days
            amount = invoice.amount_due
            
            if days_overdue <= 0:
                aging['current'] += amount
            elif days_overdue <= 30:
                aging['1-30_days'] += amount
            elif days_overdue <= 60:
                aging['31-60_days'] += amount
            elif days_overdue <= 90:
                aging['61-90_days'] += amount
            else:
                aging['over_90_days'] += amount
        
        return aging

# Helper functions for creating instances

def create_time_entry(user_id: str, matter_id: str, client_id: str, 
                     hours: float, description: str, activity_type: str = "Legal Research",
                     billing_rate: float = 250.0, billable: bool = True,
                     date: datetime = None) -> TimeEntry:
    """Create a new time entry with default values."""
    return TimeEntry(
        id=str(uuid.uuid4()),
        user_id=user_id,
        matter_id=matter_id,
        client_id=client_id,
        date=date or datetime.now(),
        hours=hours,
        description=description,
        billing_rate=billing_rate,
        billable=billable,
        activity_type=activity_type,
        status=TimeEntryStatus.DRAFT.value,
        created_date=datetime.now()
    )

def create_invoice(client_id: str, matter_id: str, line_items: List[Dict],
                  tax_rate: float = 0.08, payment_terms: str = "Net 30") -> Invoice:
    """Create a new invoice with calculated totals."""
    invoice_number = BillingCalculator.generate_invoice_number()
    due_date = datetime.now() + timedelta(days=30)  # Default to 30 days
    
    # Calculate totals
    totals = BillingCalculator.calculate_invoice_totals(line_items, tax_rate)
    
    return Invoice(
        id=str(uuid.uuid4()),
        client_id=client_id,
        matter_id=matter_id,
        invoice_number=invoice_number,
        date_issued=datetime.now(),
        due_date=due_date,
        line_items=line_items,
        subtotal=totals['subtotal'],
        tax_rate=tax_rate,
        tax_amount=totals['tax_amount'],
        total_amount=totals['total_amount'],
        status=InvoiceStatus.DRAFT.value,
        payment_terms=payment_terms
    )
