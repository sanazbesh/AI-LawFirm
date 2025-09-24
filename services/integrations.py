import streamlit as st
import requests
import json
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
import hashlib
import uuid

@dataclass
class IntegrationConfig:
    name: str
    endpoint: str
    api_key: str
    secret_key: Optional[str] = None
    is_active: bool = True
    last_sync: Optional[datetime] = None
    sync_frequency: str = "manual"  # manual, hourly, daily, weekly
    settings: Dict[str, Any] = None

@dataclass
class SyncResult:
    integration_name: str
    success: bool
    records_processed: int
    records_created: int
    records_updated: int
    records_failed: int
    error_message: Optional[str] = None
    sync_time: datetime = None
    details: Dict[str, Any] = None

class IntegrationService:
    
    def __init__(self):
        self.supported_integrations = {
            'office365': 'Microsoft Office 365',
            'google_workspace': 'Google Workspace',
            'quickbooks': 'QuickBooks Online',
            'docusign': 'DocuSign',
            'salesforce': 'Salesforce CRM',
            'dropbox': 'Dropbox Business',
            'box': 'Box',
            'slack': 'Slack',
            'zoom': 'Zoom',
            'calendly': 'Calendly',
            'lawpay': 'LawPay',
            'clio': 'Clio',
            'westlaw': 'Westlaw',
            'lexisnexis': 'LexisNexis'
        }
        
        # Initialize integration configs if not in session state
        if 'integration_configs' not in st.session_state:
            st.session_state.integration_configs = self._initialize_demo_configs()
        
        # Initialize sync history
        if 'sync_history' not in st.session_state:
            st.session_state.sync_history = []
    
    def _initialize_demo_configs(self) -> Dict[str, IntegrationConfig]:
        """Initialize demo integration configurations."""
        return {
            'office365': IntegrationConfig(
                name='Microsoft Office 365',
                endpoint='https://graph.microsoft.com/v1.0',
                api_key='demo_office365_key',
                secret_key='demo_secret',
                is_active=True,
                last_sync=datetime.now() - timedelta(hours=2),
                sync_frequency='daily',
                settings={
                    'sync_emails': True,
                    'sync_calendar': True,
                    'sync_contacts': True,
                    'tenant_id': 'demo-tenant-id'
                }
            ),
            'quickbooks': IntegrationConfig(
                name='QuickBooks Online',
                endpoint='https://sandbox-quickbooks.api.intuit.com/v3',
                api_key='demo_qb_key',
                secret_key='demo_qb_secret',
                is_active=True,
                last_sync=datetime.now() - timedelta(hours=6),
                sync_frequency='daily',
                settings={
                    'company_id': 'demo-company-123',
                    'sandbox_mode': True,
                    'sync_invoices': True,
                    'sync_payments': True
                }
            ),
            'docusign': IntegrationConfig(
                name='DocuSign',
                endpoint='https://demo.docusign.net/restapi',
                api_key='demo_docusign_key',
                is_active=True,
                last_sync=datetime.now() - timedelta(hours=1),
                sync_frequency='hourly',
                settings={
                    'account_id': 'demo-account-456',
                    'base_path': 'https://demo.docusign.net',
                    'webhook_url': 'https://yourapp.com/webhook/docusign'
                }
            ),
            'salesforce': IntegrationConfig(
                name='Salesforce CRM',
                endpoint='https://demo.salesforce.com/services/data/v58.0',
                api_key='demo_sf_key',
                is_active=False,
                settings={
                    'instance_url': 'https://demo.salesforce.com',
                    'sandbox_mode': True
                }
            )
        }
    
    def get_integration_status(self, integration_key: str) -> Dict[str, Any]:
        """Get the status of a specific integration."""
        config = st.session_state.integration_configs.get(integration_key)
        if not config:
            return {'status': 'not_configured', 'message': 'Integration not configured'}
        
        if not config.is_active:
            return {'status': 'inactive', 'message': 'Integration is disabled'}
        
        # Check connection (mock implementation)
        connection_status = self._test_connection(integration_key)
        
        return {
            'status': 'active' if connection_status else 'error',
            'message': 'Connected and syncing' if connection_status else 'Connection error',
            'last_sync': config.last_sync.isoformat() if config.last_sync else None,
            'sync_frequency': config.sync_frequency,
            'records_synced': self._get_sync_count(integration_key)
        }
    
    def _test_connection(self, integration_key: str) -> bool:
        """Test connection to integration (mock implementation)."""
        # In real implementation, this would make actual API calls
        config = st.session_state.integration_configs.get(integration_key)
        if not config:
            return False
        
        # Mock successful connection for demo
        return config.is_active
    
    def _get_sync_count(self, integration_key: str) -> int:
        """Get count of records synced for an integration."""
        # Mock implementation - count recent sync results
        return len([s for s in st.session_state.sync_history 
                   if s.integration_name == integration_key and s.success])
    
    def configure_integration(self, integration_key: str, config_data: Dict[str, Any]) -> bool:
        """Configure or update an integration."""
        try:
            if integration_key in st.session_state.integration_configs:
                # Update existing configuration
                config = st.session_state.integration_configs[integration_key]
                config.api_key = config_data.get('api_key', config.api_key)
                config.secret_key = config_data.get('secret_key', config.secret_key)
                config.endpoint = config_data.get('endpoint', config.endpoint)
                config.is_active = config_data.get('is_active', config.is_active)
                config.sync_frequency = config_data.get('sync_frequency', config.sync_frequency)
                
                if 'settings' in config_data:
                    if config.settings:
                        config.settings.update(config_data['settings'])
                    else:
                        config.settings = config_data['settings']
            else:
                # Create new configuration
                st.session_state.integration_configs[integration_key] = IntegrationConfig(
                    name=self.supported_integrations.get(integration_key, integration_key),
                    endpoint=config_data['endpoint'],
                    api_key=config_data['api_key'],
                    secret_key=config_data.get('secret_key'),
                    is_active=config_data.get('is_active', True),
                    sync_frequency=config_data.get('sync_frequency', 'manual'),
                    settings=config_data.get('settings', {})
                )
            
            return True
        except Exception as e:
            st.error(f"Failed to configure integration: {str(e)}")
            return False
    
    def sync_integration(self, integration_key: str, force_sync: bool = False) -> SyncResult:
        """Perform synchronization with an integration."""
        config = st.session_state.integration_configs.get(integration_key)
        if not config or not config.is_active:
            return SyncResult(
                integration_name=integration_key,
                success=False,
                records_processed=0,
                records_created=0,
                records_updated=0,
                records_failed=0,
                error_message="Integration not configured or inactive",
                sync_time=datetime.now()
            )
        
        # Check if sync is needed based on frequency
        if not force_sync and config.last_sync:
            time_since_sync = datetime.now() - config.last_sync
            frequency_mapping = {
                'hourly': timedelta(hours=1),
                'daily': timedelta(days=1),
                'weekly': timedelta(weeks=1)
            }
            
            required_interval = frequency_mapping.get(config.sync_frequency)
            if required_interval and time_since_sync < required_interval:
                return SyncResult(
                    integration_name=integration_key,
                    success=False,
                    records_processed=0,
                    records_created=0,
                    records_updated=0,
                    records_failed=0,
                    error_message="Sync not due yet",
                    sync_time=datetime.now()
                )
        
        # Perform actual sync based on integration type
        sync_result = self._perform_sync(integration_key, config)
        
        # Update last sync time
        config.last_sync = datetime.now()
        
        # Store sync result in history
        st.session_state.sync_history.append(sync_result)
        
        # Keep only last 100 sync results
        if len(st.session_state.sync_history) > 100:
            st.session_state.sync_history = st.session_state.sync_history[-100:]
        
        return sync_result
    
    def _perform_sync(self, integration_key: str, config: IntegrationConfig) -> SyncResult:
        """Perform the actual synchronization logic."""
        sync_time = datetime.now()
        
        try:
            if integration_key == 'office365':
                return self._sync_office365(config, sync_time)
            elif integration_key == 'quickbooks':
                return self._sync_quickbooks(config, sync_time)
            elif integration_key == 'docusign':
                return self._sync_docusign(config, sync_time)
            elif integration_key == 'salesforce':
                return self._sync_salesforce(config, sync_time)
            else:
                return self._generic_sync(integration_key, config, sync_time)
        
        except Exception as e:
            return SyncResult(
                integration_name=integration_key,
                success=False,
                records_processed=0,
                records_created=0,
                records_updated=0,
                records_failed=1,
                error_message=str(e),
                sync_time=sync_time
            )
    
    def _sync_office365(self, config: IntegrationConfig, sync_time: datetime) -> SyncResult:
        """Sync with Microsoft Office 365."""
        # Mock sync implementation
        processed = 45
        created = 3
        updated = 12
        
        return SyncResult(
            integration_name='office365',
            success=True,
            records_processed=processed,
            records_created=created,
            records_updated=updated,
            records_failed=0,
            sync_time=sync_time,
            details={
                'emails_synced': 25,
                'calendar_events_synced': 15,
                'contacts_synced': 5
            }
        )
    
    def _sync_quickbooks(self, config: IntegrationConfig, sync_time: datetime) -> SyncResult:
        """Sync with QuickBooks Online."""
        # Mock sync implementation
        processed = 23
        created = 2
        updated = 8
        
        return SyncResult(
            integration_name='quickbooks',
            success=True,
            records_processed=processed,
            records_created=created,
            records_updated=updated,
            records_failed=0,
            sync_time=sync_time,
            details={
                'invoices_synced': 15,
                'payments_synced': 8
            }
        )
    
    def _sync_docusign(self, config: IntegrationConfig, sync_time: datetime) -> SyncResult:
        """Sync with DocuSign."""
        # Mock sync implementation
        processed = 12
        created = 1
        updated = 5
        
        return SyncResult(
            integration_name='docusign',
            success=True,
            records_processed=processed,
            records_created=created,
            records_updated=updated,
            records_failed=0,
            sync_time=sync_time,
            details={
                'envelopes_synced': 8,
                'completed_documents': 4
            }
        )
    
    def _sync_salesforce(self, config: IntegrationConfig, sync_time: datetime) -> SyncResult:
        """Sync with Salesforce CRM."""
        # Mock sync implementation
        processed = 34
        created = 4
        updated = 18
        
        return SyncResult(
            integration_name='salesforce',
            success=True,
            records_processed=processed,
            records_created=created,
            records_updated=updated,
            records_failed=0,
            sync_time=sync_time,
            details={
                'leads_synced': 12,
                'opportunities_synced': 8,
                'contacts_synced': 14
            }
        )
    
    def _generic_sync(self, integration_key: str, config: IntegrationConfig, sync_time: datetime) -> SyncResult:
        """Generic sync implementation for other integrations."""
        # Mock implementation
        import random
        
        processed = random.randint(10, 50)
        created = random.randint(0, 5)
        updated = random.randint(0, processed // 2)
        
        return SyncResult(
            integration_name=integration_key,
            success=True,
            records_processed=processed,
            records_created=created,
            records_updated=updated,
            records_failed=0,
            sync_time=sync_time
        )
    
    def get_sync_history(self, integration_key: Optional[str] = None, limit: int = 50) -> List[SyncResult]:
        """Get synchronization history."""
        history = st.session_state.sync_history
        
        if integration_key:
            history = [s for s in history if s.integration_name == integration_key]
        
        # Sort by sync time (most recent first)
        history.sort(key=lambda x: x.sync_time, reverse=True)
        
        return history[:limit]
    
    def create_webhook(self, integration_key: str, webhook_url: str, events: List[str]) -> Dict[str, Any]:
        """Create a webhook for real-time integration updates."""
        config = st.session_state.integration_configs.get(integration_key)
        if not config:
            return {'success': False, 'message': 'Integration not configured'}
        
        # Mock webhook creation
        webhook_id = str(uuid.uuid4())
        
        # Store webhook configuration
        if 'webhooks' not in st.session_state:
            st.session_state.webhooks = {}
        
        st.session_state.webhooks[webhook_id] = {
            'integration_key': integration_key,
            'url': webhook_url,
            'events': events,
            'created_date': datetime.now(),
            'is_active': True
        }
        
        return {
            'success': True,
            'webhook_id': webhook_id,
            'message': 'Webhook created successfully'
        }
    
    def process_webhook(self, webhook_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming webhook data."""
        if 'webhooks' not in st.session_state:
            return {'success': False, 'message': 'Webhook not found'}
        
        webhook = st.session_state.webhooks.get(webhook_id)
        if not webhook:
            return {'success': False, 'message': 'Webhook not found'}
        
        if not webhook['is_active']:
            return {'success': False, 'message': 'Webhook is inactive'}
        
        # Process webhook payload based on integration type
        integration_key = webhook['integration_key']
        
        try:
            if integration_key == 'docusign':
                return self._process_docusign_webhook(payload)
            elif integration_key == 'quickbooks':
                return self._process_quickbooks_webhook(payload)
            else:
                return self._process_generic_webhook(integration_key, payload)
        
        except Exception as e:
            return {'success': False, 'message': f'Webhook processing error: {str(e)}'}
    
    def _process_docusign_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Process DocuSign webhook payload."""
        # Mock processing
        event_type = payload.get('event', 'unknown')
        
        if event_type == 'envelope-completed':
            # Update document status
            envelope_id = payload.get('envelopeId')
            # In real implementation, update database records
            
            return {
                'success': True,
                'message': f'Processed envelope completion: {envelope_id}',
                'action': 'document_completed'
            }
        
        return {'success': True, 'message': f'Processed event: {event_type}'}
    
    def _process_quickbooks_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Process QuickBooks webhook payload."""
        # Mock processing
        entity_name = payload.get('name', 'unknown')
        operation = payload.get('operation', 'unknown')
        
        return {
            'success': True,
            'message': f'Processed {operation} on {entity_name}',
            'action': f'qb_{operation}'
        }
    
    def _process_generic_webhook(self, integration_key: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Process generic webhook payload."""
        return {
            'success': True,
            'message': f'Processed webhook for {integration_key}',
            'action': 'generic_update'
        }
    
    def get_integration_analytics(self) -> Dict[str, Any]:
        """Get analytics for all integrations."""
        total_integrations = len(st.session_state.integration_configs)
        active_integrations = len([c for c in st.session_state.integration_configs.values() if c.is_active])
        
        # Sync statistics
        successful_syncs = len([s for s in st.session_state.sync_history if s.success])
        failed_syncs = len([s for s in st.session_state.sync_history if not s.success])
        
        # Records processed
        total_records = sum(s.records_processed for s in st.session_state.sync_history)
        records_created = sum(s.records_created for s in st.session_state.sync_history)
        records_updated = sum(s.records_updated for s in st.session_state.sync_history)
        
        # Recent activity (last 24 hours)
        recent_cutoff = datetime.now() - timedelta(hours=24)
        recent_syncs = [s for s in st.session_state.sync_history if s.sync_time and s.sync_time > recent_cutoff]
        
        return {
            'total_integrations': total_integrations,
            'active_integrations': active_integrations,
            'integration_health': (active_integrations / total_integrations * 100) if total_integrations > 0 else 0,
            'sync_success_rate': (successful_syncs / (successful_syncs + failed_syncs) * 100) if (successful_syncs + failed_syncs) > 0 else 0,
            'total_records_processed': total_records,
            'records_created': records_created,
            'records_updated': records_updated,
            'recent_sync_count': len(recent_syncs),
            'last_sync_time': max([s.sync_time for s in st.session_state.sync_history if s.sync_time], default=None)
        }
    
    def export_integration_data(self, integration_key: str, data_type: str, date_range: tuple = None) -> Dict[str, Any]:
        """Export data from an integration."""
        config = st.session_state.integration_configs.get(integration_key)
        if not config or not config.is_active:
            return {'success': False, 'message': 'Integration not available'}
        
        # Mock export functionality
        export_id = str(uuid.uuid4())
        
        # Simulate export process
        record_count = {
            'contacts': 150,
            'emails': 500,
            'invoices': 75,
            'documents': 200
        }.get(data_type, 100)
        
        return {
            'success': True,
            'export_id': export_id,
            'records_exported': record_count,
            'format': 'json',
            'message': f'Export initiated for {record_count} {data_type} records'
        }
    
    def schedule_sync(self, integration_key: str, frequency: str, start_time: datetime = None) -> bool:
        """Schedule automatic synchronization for an integration."""
        config = st.session_state.integration_configs.get(integration_key)
        if not config:
            return False
        
        config.sync_frequency = frequency
        
        # In a real implementation, this would set up actual scheduled tasks
        # For demo, we just update the configuration
        
        return True
    
    def get_supported_integrations(self) -> Dict[str, Dict[str, Any]]:
        """Get list of all supported integrations with their capabilities."""
        return {
            key: {
                'name': name,
                'configured': key in st.session_state.integration_configs,
                'active': st.session_state.integration_configs.get(key, {}).is_active if key in st.session_state.integration_configs else False,
                'capabilities': self._get_integration_capabilities(key)
            }
            for key, name in self.supported_integrations.items()
        }
    
    def _get_integration_capabilities(self, integration_key: str) -> List[str]:
        """Get capabilities for a specific integration."""
        capabilities = {
            'office365': ['Email Sync', 'Calendar Sync', 'Contact Sync', 'Document Storage'],
            'google_workspace': ['Email Sync', 'Calendar Sync', 'Contact Sync', 'Drive Integration'],
            'quickbooks': ['Invoice Sync', 'Payment Sync', 'Client Sync', 'Expense Tracking'],
            'docusign': ['Document Signing', 'Envelope Tracking', 'Template Management'],
            'salesforce': ['Lead Management', 'Contact Sync', 'Opportunity Tracking'],
            'dropbox': ['Document Storage', 'File Sharing', 'Version Control'],
            'box': ['Document Storage', 'Collaboration', 'Security Controls'],
            'slack': ['Team Communication', 'File Sharing', 'Notifications'],
            'zoom': ['Video Conferencing', 'Meeting Scheduling', 'Recording'],
            'calendly': ['Appointment Scheduling', 'Calendar Integration'],
            'lawpay': ['Payment Processing', 'Trust Account Management'],
            'clio': ['Practice Management', 'Time Tracking', 'Billing'],
            'westlaw': ['Legal Research', 'Case Law Access'],
            'lexisnexis': ['Legal Research', 'Document Analysis']
        }
        
        return capabilities.get(integration_key, ['Data Sync', 'API Access'])
    
    def test_all_integrations(self) -> Dict[str, Dict[str, Any]]:
        """Test connectivity for all configured integrations."""
        results = {}
        
        for key, config in st.session_state.integration_configs.items():
            if config.is_active:
                # Mock test results
                test_success = True  # In real implementation, would make actual API calls
                
                results[key] = {
                    'name': config.name,
                    'success': test_success,
                    'response_time': 0.15,  # Mock response time
                    'last_tested': datetime.now().isoformat(),
                    'error_message': None if test_success else 'Connection timeout'
                }
            else:
                results[key] = {
                    'name': config.name,
                    'success': False,
                    'response_time': None,
                    'last_tested': datetime.now().isoformat(),
                    'error_message': 'Integration is disabled'
                }
        
        return results
