from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid
import hashlib

class UserRole(Enum):
    ADMIN = "admin"
    PARTNER = "partner"
    SENIOR_ASSOCIATE = "senior_associate"
    ASSOCIATE = "associate"
    PARALEGAL = "paralegal"
    SECRETARY = "secretary"
    BILLING_CLERK = "billing_clerk"
    IT_SUPPORT = "it_support"
    CLIENT = "client"

class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_ACTIVATION = "pending_activation"
    LOCKED = "locked"

class ClientType(Enum):
    INDIVIDUAL = "individual"
    CORPORATION = "corporation"
    NON_PROFIT = "non_profit"
    GOVERNMENT = "government"
    PARTNERSHIP = "partnership"
    LLC = "llc"
    TRUST = "trust"
    OTHER = "other"

class ClientStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PROSPECTIVE = "prospective"
    FORMER = "former"
    SUSPENDED = "suspended"

@dataclass
class UserPreferences:
    theme: str = "light"  # light, dark
    language: str = "en"
    timezone: str = "UTC"
    date_format: str = "MM/DD/YYYY"
    time_format: str = "12h"  # 12h, 24h
    notifications_email: bool = True
    notifications_browser: bool = True
    default_billing_rate: float = 0.0
    dashboard_layout: Dict[str, Any] = field(default_factory=dict)

@dataclass
class UserPermissions:
    can_create_matters: bool = False
    can_edit_matters: bool = False
    can_delete_matters: bool = False
    can_view_all_matters: bool = False
    can_manage_clients: bool = False
    can_access_billing: bool = False
    can_generate_reports: bool = False
    can_manage_users: bool = False
    can_access_admin: bool = False
    can_approve_timesheets: bool = False
    custom_permissions: Dict[str, bool] = field(default_factory=dict)

@dataclass
class LoginAttempt:
    timestamp: datetime
    ip_address: str
    user_agent: str
    success: bool
    failure_reason: Optional[str] = None

@dataclass
class UserSession:
    session_id: str
    created_date: datetime
    last_activity: datetime
    ip_address: str
    user_agent: str
    is_active: bool = True

@dataclass
class User:
    id: str
    email: str
    role: str
    created_date: datetime
    last_login: datetime
    
    # Enhanced fields
    first_name: str = ""
    last_name: str = ""
    username: str = ""
    password_hash: str = ""
    phone: str = ""
    mobile: str = ""
    office_location: str = ""
    department: str = ""
    title: str = ""
    employee_id: str = ""
    bar_number: str = ""
    
    # Status and security
    status: str = UserStatus.ACTIVE.value
    is_verified: bool = False
    two_factor_enabled: bool = False
    password_reset_token: Optional[str] = None
    password_reset_expires: Optional[datetime] = None
    failed_login_attempts: int = 0
    account_locked_until: Optional[datetime] = None
    
    # Profile information
    avatar_url: str = ""
    bio: str = ""
    skills: List[str] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    languages: List[str] = field(default_factory=list)
    
    # Preferences and permissions
    preferences: UserPreferences = field(default_factory=UserPreferences)
    permissions: UserPermissions = field(default_factory=UserPermissions)
    
    # Activity tracking
    login_attempts: List[LoginAttempt] = field(default_factory=list)
    active_sessions: List[UserSession] = field(default_factory=list)
    
    # Metadata
    created_by: str = ""
    last_modified: datetime = field(default_factory=datetime.now)
    last_modified_by: str = ""
    notes: str = ""
    
    def __post_init__(self):
        """Post-initialization processing."""
        if not self.username and self.email:
            self.username = self.email.split('@')[0]
        
        # Set default permissions based on role
        self._set_default_permissions()
    
    @property
    def full_name(self) -> str:
        """Get the user's full name."""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def display_name(self) -> str:
        """Get the display name (full name or email if no name)."""
        if self.full_name:
            return self.full_name
        return self.email
    
    @property
    def is_active(self) -> bool:
        """Check if the user is active."""
        return self.status == UserStatus.ACTIVE.value
    
    @property
    def is_locked(self) -> bool:
        """Check if the user account is locked."""
        if self.account_locked_until and datetime.now() < self.account_locked_until:
            return True
        if self.status == UserStatus.LOCKED.value:
            return True
        return False
    
    @property
    def is_attorney(self) -> bool:
        """Check if the user is an attorney."""
        attorney_roles = [UserRole.PARTNER.value, UserRole.SENIOR_ASSOCIATE.value, UserRole.ASSOCIATE.value]
        return self.role in attorney_roles
    
    @property
    def days_since_last_login(self) -> int:
        """Calculate days since last login."""
        if not self.last_login:
            return 0
        return (datetime.now() - self.last_login).days
    
    def _set_default_permissions(self) -> None:
        """Set default permissions based on user role."""
        role_permissions = {
            UserRole.ADMIN.value: {
                "can_create_matters": True,
                "can_edit_matters": True,
                "can_delete_matters": True,
                "can_view_all_matters": True,
                "can_manage_clients": True,
                "can_access_billing": True,
                "can_generate_reports": True,
                "can_manage_users": True,
                "can_access_admin": True,
                "can_approve_timesheets": True
            },
            UserRole.PARTNER.value: {
                "can_create_matters": True,
                "can_edit_matters": True,
                "can_delete_matters": True,
                "can_view_all_matters": True,
                "can_manage_clients": True,
                "can_access_billing": True,
                "can_generate_reports": True,
                "can_manage_users": False,
                "can_access_admin": False,
                "can_approve_timesheets": True
            },
            UserRole.ASSOCIATE.value: {
                "can_create_matters": False,
                "can_edit_matters": True,
                "can_delete_matters": False,
                "can_view_all_matters": False,
                "can_manage_clients": False,
                "can_access_billing": False,
                "can_generate_reports": False,
                "can_manage_users": False,
                "can_access_admin": False,
                "can_approve_timesheets": False
            }
        }
        
        if self.role in role_permissions:
            for permission, value in role_permissions[self.role].items():
                setattr(self.permissions, permission, value)
    
    def set_password(self, password: str) -> None:
        """Set the user's password (hashed)."""
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.last_modified = datetime.now()
    
    def verify_password(self, password: str) -> bool:
        """Verify the user's password."""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return self.password_hash == password_hash
    
    def record_login_attempt(self, ip_address: str, user_agent: str, success: bool, failure_reason: str = None) -> None:
        """Record a login attempt."""
        attempt = LoginAttempt(
            timestamp=datetime.now(),
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            failure_reason=failure_reason
        )
        
        self.login_attempts.append(attempt)
        
        if success:
            self.last_login = datetime.now()
            self.failed_login_attempts = 0
            if self.account_locked_until:
                self.account_locked_until = None
        else:
            self.failed_login_attempts += 1
            if self.failed_login_attempts >= 5:  # Lock after 5 failed attempts
                self.account_locked_until = datetime.now() + timedelta(minutes=30)
    
    def create_session(self, ip_address: str, user_agent: str) -> UserSession:
        """Create a new user session."""
        session = UserSession(
            session_id=str(uuid.uuid4()),
            created_date=datetime.now(),
            last_activity=datetime.now(),
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        self.active_sessions.append(session)
        return session
    
    def end_session(self, session_id: str) -> bool:
        """End a specific session."""
        for session in self.active_sessions:
            if session.session_id == session_id:
                session.is_active = False
                return True
        return False
    
    def end_all_sessions(self) -> None:
        """End all active sessions."""
        for session in self.active_sessions:
            session.is_active = False
    
    def update_preferences(self, **kwargs) -> None:
        """Update user preferences."""
        for key, value in kwargs.items():
            if hasattr(self.preferences, key):
                setattr(self.preferences, key, value)
        self.last_modified = datetime.now()
    
    def grant_permission(self, permission: str, granted_by: str) -> None:
        """Grant a specific permission to the user."""
        if hasattr(self.permissions, permission):
            setattr(self.permissions, permission, True)
        else:
            self.permissions.custom_permissions[permission] = True
        
        self.last_modified = datetime.now()
        self.last_modified_by = granted_by
    
    def revoke_permission(self, permission: str, revoked_by: str) -> None:
        """Revoke a specific permission from the user."""
        if hasattr(self.permissions, permission):
            setattr(self.permissions, permission, False)
        else:
            self.permissions.custom_permissions[permission] = False
        
        self.last_modified = datetime.now()
        self.last_modified_by = revoked_by
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission."""
        if hasattr(self.permissions, permission):
            return getattr(self.permissions, permission)
        return self.permissions.custom_permissions.get(permission, False)

@dataclass
class ClientContact:
    contact_type: str  # primary, billing, emergency
    name: str
    title: str = ""
    email: str = ""
    phone: str = ""
    mobile: str = ""
    address: str = ""
    notes: str = ""
    is_primary: bool = False

@dataclass
class ClientBilling:
    billing_method: str = "email"  # email, mail, portal
    billing_frequency: str = "monthly"  # monthly, quarterly, project
    payment_terms: str = "net_30"
    preferred_payment_method: str = "check"
    billing_address: str = ""
    tax_id: str = ""
    credit_limit: float = 0.0
    current_balance: float = 0.0
    
@dataclass 
class ClientEngagement:
    start_date: datetime
    end_date: Optional[datetime] = None
    engagement_letter_signed: bool = False
    conflicts_checked: bool = False
    intake_completed: bool = False
    notes: str = ""

@dataclass
class Client:
    id: str
    name: str
    client_type: str
    contact_info: Dict
    created_date: datetime
    status: str
    portal_access: bool
    
    # Enhanced fields
    client_number: str = ""
    company_name: str = ""
    industry: str = ""
    website: str = ""
    tax_id: str = ""
    
    # Primary contact information
    primary_email: str = ""
    primary_phone: str = ""
    primary_address: str = ""
    
    # Additional contacts
    contacts: List[ClientContact] = field(default_factory=list)
    
    # Billing information
    billing_info: ClientBilling = field(default_factory=ClientBilling)
    
    # Engagement details
    engagement: ClientEngagement = field(default_factory=lambda: ClientEngagement(start_date=datetime.now()))
    
    # Portal and access
    portal_user_id: Optional[str] = None
    portal_last_login: Optional[datetime] = None
    document_access_level: str = "standard"  # standard, restricted, full
    
    # Financial tracking
    total_billed: float = 0.0
    total_paid: float = 0.0
    outstanding_balance: float = 0.0
    credit_rating: str = "good"  # excellent, good, fair, poor
    
    # Metadata and tracking
    source: str = ""  # referral, website, marketing, etc.
    referral_source: str = ""
    tags: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    
    # Activity tracking
    created_by: str = ""
    last_modified: datetime = field(default_factory=datetime.now)
    last_modified_by: str = ""
    last_contact_date: Optional[datetime] = None
    next_follow_up: Optional[datetime] = None
    
    def __post_init__(self):
        """Post-initialization processing."""
        if not self.client_number:
            self.client_number = self.generate_client_number()
        
        # Extract primary contact info from contact_info dict if provided
        if self.contact_info:
            self.primary_email = self.contact_info.get('email', self.primary_email)
            self.primary_phone = self.contact_info.get('phone', self.primary_phone)
            self.primary_address = self.contact_info.get('address', self.primary_address)
    
    @property
    def is_active(self) -> bool:
        """Check if the client is active."""
        return self.status == ClientStatus.ACTIVE.value
    
    @property
    def is_corporate(self) -> bool:
        """Check if this is a corporate client."""
        corporate_types = [ClientType.CORPORATION.value, ClientType.LLC.value, ClientType.PARTNERSHIP.value]
        return self.client_type in corporate_types
    
    @property
    def collection_rate(self) -> float:
        """Calculate the collection rate percentage."""
        if self.total_billed == 0:
            return 0.0
        return (self.total_paid / self.total_billed) * 100
    
    @property
    def days_since_created(self) -> int:
        """Calculate days since client was created."""
        return (datetime.now() - self.created_date).days
    
    @property
    def days_since_last_contact(self) -> int:
        """Calculate days since last contact."""
        if not self.last_contact_date:
            return 0
        return (datetime.now() - self.last_contact_date).days
    
    @property
    def primary_contact(self) -> Optional[ClientContact]:
        """Get the primary contact."""
        for contact in self.contacts:
            if contact.is_primary:
                return contact
        return None
    
    def generate_client_number(self) -> str:
        """Generate a unique client number."""
        year = self.created_date.year
        # Simple format: YYYY-CCCC (year + 4-digit sequential)
        return f"{year}-{str(uuid.uuid4())[:4].upper()}"
    
    def add_contact(self, contact_type: str, name: str, email: str = "", 
                   phone: str = "", is_primary: bool = False, **kwargs) -> ClientContact:
        """Add a contact to the client."""
        # If setting as primary, unset other primary contacts
        if is_primary:
            for contact in self.contacts:
                contact.is_primary = False
        
        contact = ClientContact(
            contact_type=contact_type,
            name=name,
            email=email,
            phone=phone,
            is_primary=is_primary,
            **kwargs
        )
        
        self.contacts.append(contact)
        self.last_modified = datetime.now()
        return contact
    
    def update_billing_info(self, **kwargs) -> None:
        """Update billing information."""
        for key, value in kwargs.items():
            if hasattr(self.billing_info, key):
                setattr(self.billing_info, key, value)
        self.last_modified = datetime.now()
    
    def record_payment(self, amount: float, payment_date: datetime = None) -> None:
        """Record a payment from the client."""
        self.total_paid += amount
        self.outstanding_balance = max(0, self.outstanding_balance - amount)
        self.billing_info.current_balance = max(0, self.billing_info.current_balance - amount)
        self.last_modified = datetime.now()
    
    def add_invoice(self, amount: float, invoice_date: datetime = None) -> None:
        """Add an invoice amount to the client's billing."""
        self.total_billed += amount
        self.outstanding_balance += amount
        self.billing_info.current_balance += amount
        self.last_modified = datetime.now()
    
    def update_portal_access(self, has_access: bool, access_level: str = "standard") -> None:
        """Update client portal access."""
        self.portal_access = has_access
        self.document_access_level = access_level
        self.last_modified = datetime.now()
    
    def record_portal_login(self) -> None:
        """Record a portal login."""
        self.portal_last_login = datetime.now()
    
    def add_note(self, note: str, author: str) -> None:
        """Add a note about the client."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        formatted_note = f"[{timestamp}] {author}: {note}"
        self.notes.append(formatted_note)
        self.last_modified = datetime.now()
        self.last_modified_by = author
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the client."""
        if tag not in self.tags:
            self.tags.append(tag)
            self.last_modified = datetime.now()
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the client."""
        if tag in self.tags:
            self.tags.remove(tag)
            self.last_modified = datetime.now()
    
    def update_contact_date(self, contact_date: datetime = None) -> None:
        """Update the last contact date."""
        self.last_contact_date = contact_date or datetime.now()
        self.last_modified = datetime.now()
    
    def set_follow_up(self, follow_up_date: datetime, notes: str = "") -> None:
        """Set a follow-up date."""
        self.next_follow_up = follow_up_date
        if notes:
            self.add_note(f"Follow-up scheduled for {follow_up_date.strftime('%Y-%m-%d')}: {notes}", "system")
    
    def get_client_summary(self) -> Dict[str, Any]:
        """Get a summary of the client."""
        return {
            "id": self.id,
            "name": self.name,
            "client_number": self.client_number,
            "client_type": self.client_type,
            "status": self.status,
            "days_since_created": self.days_since_created,
            "days_since_last_contact": self.days_since_last_contact,
            "total_billed": self.total_billed,
            "total_paid": self.total_paid,
            "outstanding_balance": self.outstanding_balance,
            "collection_rate": round(self.collection_rate, 2),
            "portal_access": self.portal_access,
            "portal_last_login": self.portal_last_login,
            "contact_count": len(self.contacts),
            "tags": self.tags,
            "created_date": self.created_date,
            "last_modified": self.last_modified
        }

class UserManager:
    """Utility class for user operations."""
    
    @staticmethod
    def create_user(email: str, role: str, first_name: str = "", last_name: str = "",
                   created_by: str = "system") -> User:
        """Create a new user with default values."""
        user_id = str(uuid.uuid4())
        current_time = datetime.now()
        
        user = User(
            id=user_id,
            email=email,
            role=role,
            created_date=current_time,
            last_login=current_time,
            first_name=first_name,
            last_name=last_name,
            created_by=created_by,
            last_modified_by=created_by
        )
        
        return user
    
    @staticmethod
    def create_client(name: str, client_type: str, created_by: str = "system",
                     contact_info: Dict = None) -> Client:
        """Create a new client with default values."""
        client_id = str(uuid.uuid4())
        current_time = datetime.now()
        
        client = Client(
            id=client_id,
            name=name,
            client_type=client_type,
            contact_info=contact_info or {},
            created_date=current_time,
            status=ClientStatus.ACTIVE.value,
            portal_access=False,
            created_by=created_by,
            last_modified_by=created_by
        )
        
        return client
