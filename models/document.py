from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
import uuid

class DocumentStatus(Enum):
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    FINAL = "final"
    ARCHIVED = "archived"
    DELETED = "deleted"

class DocumentType(Enum):
    CONTRACT = "contract"
    BRIEF = "brief"
    MOTION = "motion"
    CORRESPONDENCE = "correspondence"
    DISCOVERY = "discovery"
    PLEADING = "pleading"
    MEMO = "memo"
    AGREEMENT = "agreement"
    COURT_FILING = "court_filing"
    RESEARCH = "research"
    TEMPLATE = "template"
    OTHER = "other"

class SecurityLevel(Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    PRIVILEGED = "privileged"
    RESTRICTED = "restricted"

class AccessLevel(Enum):
    READ_ONLY = "read_only"
    EDIT = "edit"
    COMMENT = "comment"
    FULL_ACCESS = "full_access"
    NO_ACCESS = "no_access"

@dataclass
class DocumentVersion:
    version_number: str
    created_date: datetime
    created_by: str
    file_path: str
    file_size: int
    checksum: str
    change_summary: Optional[str] = None
    is_current: bool = False

@dataclass
class DocumentAccess:
    user_id: str
    access_level: str
    granted_by: str
    granted_date: datetime
    expires_date: Optional[datetime] = None
    notes: Optional[str] = None

@dataclass
class DocumentAnnotation:
    id: str
    user_id: str
    page_number: Optional[int] = None
    position: Optional[Dict[str, Any]] = None
    annotation_type: str = "comment"  # comment, highlight, note, redaction
    content: str = ""
    created_date: datetime = field(default_factory=datetime.now)
    is_resolved: bool = False

@dataclass
class DocumentActivity:
    id: str
    user_id: str
    action: str  # created, viewed, edited, shared, deleted, etc.
    timestamp: datetime
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None

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
    
    # Enhanced fields
    created_by: str = ""
    modified_by: str = ""
    file_path: str = ""
    file_size: int = 0
    file_format: str = ""
    mime_type: str = ""
    security_level: str = SecurityLevel.INTERNAL.value
    retention_date: Optional[datetime] = None
    parent_document_id: Optional[str] = None
    category: str = ""
    subcategory: str = ""
    language: str = "en"
    page_count: int = 0
    word_count: int = 0
    checksum: str = ""
    
    # Relationships
    versions: List[DocumentVersion] = field(default_factory=list)
    access_permissions: List[DocumentAccess] = field(default_factory=list)
    annotations: List[DocumentAnnotation] = field(default_factory=list)
    activity_log: List[DocumentActivity] = field(default_factory=list)
    
    # Metadata and analysis
    metadata: Dict[str, Any] = field(default_factory=dict)
    ai_analysis: Dict[str, Any] = field(default_factory=dict)
    ocr_confidence: float = 0.0
    
    def __post_init__(self):
        """Post-initialization processing."""
        if not self.created_by and not self.modified_by:
            self.created_by = "system"
            self.modified_by = "system"
    
    @property
    def is_current_version(self) -> bool:
        """Check if this is the current version."""
        return len(self.versions) == 0 or any(v.is_current for v in self.versions)
    
    @property
    def is_confidential(self) -> bool:
        """Check if document has confidential or higher security level."""
        confidential_levels = [SecurityLevel.CONFIDENTIAL.value, SecurityLevel.PRIVILEGED.value, SecurityLevel.RESTRICTED.value]
        return self.security_level in confidential_levels
    
    @property
    def days_since_created(self) -> int:
        """Calculate days since document was created."""
        return (datetime.now() - self.created_date).days
    
    @property
    def days_since_modified(self) -> int:
        """Calculate days since document was last modified."""
        return (datetime.now() - self.last_modified).days
    
    @property
    def is_recent(self) -> bool:
        """Check if document was created or modified in the last 7 days."""
        return self.days_since_created <= 7 or self.days_since_modified <= 7
    
    def add_version(self, created_by: str, file_path: str, file_size: int, 
                   checksum: str, change_summary: str = None) -> DocumentVersion:
        """Add a new version of the document."""
        # Mark all existing versions as not current
        for version in self.versions:
            version.is_current = False
        
        # Create new version
        version_number = f"{len(self.versions) + 1}.0"
        new_version = DocumentVersion(
            version_number=version_number,
            created_date=datetime.now(),
            created_by=created_by,
            file_path=file_path,
            file_size=file_size,
            checksum=checksum,
            change_summary=change_summary,
            is_current=True
        )
        
        self.versions.append(new_version)
        self.current_version = version_number
        self.last_modified = datetime.now()
        self.modified_by = created_by
        self.file_path = file_path
        self.file_size = file_size
        self.checksum = checksum
        
        # Log activity
        self.log_activity(created_by, "version_created", {"version": version_number})
        
        return new_version
    
    def grant_access(self, user_id: str, access_level: str, granted_by: str,
                    expires_date: datetime = None, notes: str = None) -> None:
        """Grant access to a user."""
        # Remove existing access for this user
        self.access_permissions = [ap for ap in self.access_permissions if ap.user_id != user_id]
        
        # Add new access permission
        new_access = DocumentAccess(
            user_id=user_id,
            access_level=access_level,
            granted_by=granted_by,
            granted_date=datetime.now(),
            expires_date=expires_date,
            notes=notes
        )
        
        self.access_permissions.append(new_access)
        self.log_activity(granted_by, "access_granted", {"user_id": user_id, "access_level": access_level})
    
    def revoke_access(self, user_id: str, revoked_by: str) -> None:
        """Revoke access for a user."""
        self.access_permissions = [ap for ap in self.access_permissions if ap.user_id != user_id]
        self.log_activity(revoked_by, "access_revoked", {"user_id": user_id})
    
    def get_user_access_level(self, user_id: str) -> Optional[str]:
        """Get the access level for a specific user."""
        current_time = datetime.now()
        
        for access in self.access_permissions:
            if access.user_id == user_id:
                # Check if access has expired
                if access.expires_date and current_time > access.expires_date:
                    continue
                return access.access_level
        
        return None
    
    def can_user_access(self, user_id: str, required_level: str = AccessLevel.READ_ONLY.value) -> bool:
        """Check if a user can access the document with the required level."""
        user_level = self.get_user_access_level(user_id)
        if not user_level:
            return False
        
        # Define access hierarchy
        access_hierarchy = {
            AccessLevel.NO_ACCESS.value: 0,
            AccessLevel.READ_ONLY.value: 1,
            AccessLevel.COMMENT.value: 2,
            AccessLevel.EDIT.value: 3,
            AccessLevel.FULL_ACCESS.value: 4
        }
        
        user_level_value = access_hierarchy.get(user_level, 0)
        required_level_value = access_hierarchy.get(required_level, 0)
        
        return user_level_value >= required_level_value
    
    def add_annotation(self, user_id: str, content: str, annotation_type: str = "comment",
                      page_number: int = None, position: Dict = None) -> DocumentAnnotation:
        """Add an annotation to the document."""
        annotation = DocumentAnnotation(
            id=str(uuid.uuid4()),
            user_id=user_id,
            page_number=page_number,
            position=position,
            annotation_type=annotation_type,
            content=content
        )
        
        self.annotations.append(annotation)
        self.log_activity(user_id, "annotation_added", {"annotation_id": annotation.id})
        
        return annotation
    
    def resolve_annotation(self, annotation_id: str, resolved_by: str) -> bool:
        """Mark an annotation as resolved."""
        for annotation in self.annotations:
            if annotation.id == annotation_id:
                annotation.is_resolved = True
                self.log_activity(resolved_by, "annotation_resolved", {"annotation_id": annotation_id})
                return True
        return False
    
    def get_unresolved_annotations(self) -> List[DocumentAnnotation]:
        """Get all unresolved annotations."""
        return [ann for ann in self.annotations if not ann.is_resolved]
    
    def log_activity(self, user_id: str, action: str, details: Dict = None, ip_address: str = None) -> None:
        """Log an activity on the document."""
        activity = DocumentActivity(
            id=str(uuid.uuid4()),
            user_id=user_id,
            action=action,
            timestamp=datetime.now(),
            details=details,
            ip_address=ip_address
        )
        
        self.activity_log.append(activity)
        self.last_modified = datetime.now()
        self.modified_by = user_id
    
    def update_status(self, new_status: str, updated_by: str, notes: str = None) -> None:
        """Update the document status."""
        old_status = self.status
        self.status = new_status
        self.log_activity(updated_by, "status_changed", {
            "old_status": old_status,
            "new_status": new_status,
            "notes": notes
        })
    
    def add_tag(self, tag: str, added_by: str) -> None:
        """Add a tag to the document."""
        if tag not in self.tags:
            self.tags.append(tag)
            self.log_activity(added_by, "tag_added", {"tag": tag})
    
    def remove_tag(self, tag: str, removed_by: str) -> None:
        """Remove a tag from the document."""
        if tag in self.tags:
            self.tags.remove(tag)
            self.log_activity(removed_by, "tag_removed", {"tag": tag})
    
    def set_security_level(self, security_level: str, set_by: str, reason: str = None) -> None:
        """Set the security level of the document."""
        old_level = self.security_level
        self.security_level = security_level
        self.log_activity(set_by, "security_level_changed", {
            "old_level": old_level,
            "new_level": security_level,
            "reason": reason
        })
    
    def extract_key_information(self) -> Dict[str, Any]:
        """Extract and update key information from the document."""
        # This would typically involve AI/NLP processing
        # For now, return basic information
        info = {
            "document_type": self.document_type,
            "page_count": self.page_count,
            "word_count": self.word_count,
            "creation_date": self.created_date.isoformat(),
            "tags": self.tags,
            "security_level": self.security_level,
            "is_privileged": self.is_privileged
        }
        
        # Update the key_information field
        self.key_information.update(info)
        return self.key_information
    
    def get_related_documents(self, documents: List['Document']) -> List['Document']:
        """Find documents related to this one based on various criteria."""
        related = []
        
        for doc in documents:
            if doc.id == self.id:
                continue
            
            # Same matter
            if doc.matter_id == self.matter_id:
                related.append(doc)
                continue
            
            # Same client
            if doc.client_name == self.client_name:
                related.append(doc)
                continue
            
            # Shared tags
            common_tags = set(self.tags) & set(doc.tags)
            if len(common_tags) >= 2:
                related.append(doc)
                continue
            
            # Parent-child relationship
            if doc.parent_document_id == self.id or self.parent_document_id == doc.id:
                related.append(doc)
        
        return related
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert document to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "matter_id": self.matter_id,
            "client_name": self.client_name,
            "document_type": self.document_type,
            "current_version": self.current_version,
            "status": self.status,
            "tags": self.tags,
            "security_level": self.security_level,
            "created_date": self.created_date.isoformat(),
            "last_modified": self.last_modified.isoformat(),
            "created_by": self.created_by,
            "modified_by": self.modified_by,
            "file_size": self.file_size,
            "file_format": self.file_format,
            "page_count": self.page_count,
            "word_count": self.word_count,
            "is_privileged": self.is_privileged,
            "is_confidential": self.is_confidential,
            "days_since_created": self.days_since_created,
            "days_since_modified": self.days_since_modified,
            "version_count": len(self.versions),
            "annotation_count": len(self.annotations),
            "unresolved_annotations": len(self.get_unresolved_annotations())
        }

@dataclass
class DocumentSearchCriteria:
    """Criteria for searching documents."""
    text_query: Optional[str] = None
    document_types: List[str] = field(default_factory=list)
    statuses: List[str] = field(default_factory=list)
    security_levels: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    matter_ids: List[str] = field(default_factory=list)
    client_names: List[str] = field(default_factory=list)
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
    modified_after: Optional[datetime] = None
    modified_before: Optional[datetime] = None
    created_by: Optional[str] = None
    modified_by: Optional[str] = None
    min_file_size: Optional[int] = None
    max_file_size: Optional[int] = None
    has_annotations: Optional[bool] = None
    is_privileged: Optional[bool] = None

class DocumentManager:
    """Utility class for document operations."""
    
    @staticmethod
    def create_document(name: str, matter_id: str, client_name: str, 
                       document_type: str, created_by: str,
                       file_path: str = "", file_size: int = 0,
                       security_level: str = SecurityLevel.INTERNAL.value) -> Document:
        """Create a new document with default values."""
        doc_id = str(uuid.uuid4())
        current_time = datetime.now()
        
        document = Document(
            id=doc_id,
            name=name,
            matter_id=matter_id,
            client_name=client_name,
            document_type=document_type,
            current_version="1.0",
            status=DocumentStatus.DRAFT.value,
            tags=[],
            extracted_text="",
            key_information={},
            created_date=current_time,
            last_modified=current_time,
            is_privileged=security_level == SecurityLevel.PRIVILEGED.value,
            created_by=created_by,
            modified_by=created_by,
            file_path=file_path,
            file_size=file_size,
            security_level=security_level
        )
        
        # Log creation activity
        document.log_activity(created_by, "document_created", {"document_id": doc_id})
        
        return document
    
    @staticmethod
    def filter_documents(documents: List[Document], criteria: DocumentSearchCriteria) -> List[Document]:
        """Filter documents based on search criteria."""
        filtered = documents
        
        if criteria.text_query:
            query_lower = criteria.text_query.lower()
            filtered = [
                doc for doc in filtered
                if query_lower in doc.name.lower() or 
                   query_lower in doc.extracted_text.lower() or
                   any(query_lower in tag.lower() for tag in doc.tags)
            ]
        
        if criteria.document_types:
            filtered = [doc for doc in filtered if doc.document_type in criteria.document_types]
        
        if criteria.statuses:
            filtered = [doc for doc in filtered if doc.status in criteria.statuses]
        
        if criteria.security_levels:
            filtered = [doc for doc in filtered if doc.security_level in criteria.security_levels]
        
        if criteria.tags:
            filtered = [
                doc for doc in filtered
                if any(tag in doc.tags for tag in criteria.tags)
            ]
        
        if criteria.matter_ids:
            filtered = [doc for doc in filtered if doc.matter_id in criteria.matter_ids]
        
        if criteria.client_names:
            filtered = [doc for doc in filtered if doc.client_name in criteria.client_names]
        
        if criteria.created_after:
            filtered = [doc for doc in filtered if doc.created_date >= criteria.created_after]
        
        if criteria.created_before:
            filtered = [doc for doc in filtered if doc.created_date <= criteria.created_before]
        
        if criteria.modified_after:
            filtered = [doc for doc in filtered if doc.last_modified >= criteria.modified_after]
        
        if criteria.modified_before:
            filtered = [doc for doc in filtered if doc.last_modified <= criteria.modified_before]
        
        if criteria.created_by:
            filtered = [doc for doc in filtered if doc.created_by == criteria.created_by]
        
        if criteria.modified_by:
            filtered = [doc for doc in filtered if doc.modified_by == criteria.modified_by]
        
        if criteria.min_file_size is not None:
            filtered = [doc for doc in filtered if doc.file_size >= criteria.min_file_size]
        
        if criteria.max_file_size is not None:
            filtered = [doc for doc in filtered if doc.file_size <= criteria.max_file_size]
        
        if criteria.has_annotations is not None:
            filtered = [
                doc for doc in filtered
                if bool(doc.annotations) == criteria.has_annotations
            ]
        
        if criteria.is_privileged is not None:
            filtered = [doc for doc in filtered if doc.is_privileged == criteria.is_privileged]
        
        return filtered
    
    @staticmethod
    def get_document_statistics(documents: List[Document]) -> Dict[str, Any]:
        """Generate statistics for a collection of documents."""
        if not documents:
            return {}
        
        total_docs = len(documents)
        total_size = sum(doc.file_size for doc in documents)
        total_pages = sum(doc.page_count for doc in documents)
        
        # Status distribution
        status_counts = {}
        for doc in documents:
            status_counts[doc.status] = status_counts.get(doc.status, 0) + 1
        
        # Document type distribution
        type_counts = {}
        for doc in documents:
            type_counts[doc.document_type] = type_counts.get(doc.document_type, 0) + 1
        
        # Security level distribution
        security_counts = {}
        for doc in documents:
            security_counts[doc.security_level] = security_counts.get(doc.security_level, 0) + 1
        
        return {
            "total_documents": total_docs,
            "total_file_size": total_size,
            "total_pages": total_pages,
            "average_file_size": total_size / total_docs if total_docs > 0 else 0,
            "status_distribution": status_counts,
            "type_distribution": type_counts,
            "security_distribution": security_counts,
            "privileged_documents": sum(1 for doc in documents if doc.is_privileged),
            "recent_documents": sum(1 for doc in documents if doc.is_recent),
            "documents_with_annotations": sum(1 for doc in documents if doc.annotations)
        }
