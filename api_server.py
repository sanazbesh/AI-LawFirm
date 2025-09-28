from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
import os
import sys
import json
import uuid
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'
CORS(app, supports_credentials=True)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'doc'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory storage (replace with database in production)
users_db = {}
sessions_db = {}
documents_db = []
matters_db = []
clients_db = []
time_entries_db = []

# Initialize with sample data
def initialize_sample_data():
    # Sample clients
    clients_db.extend([
        {
            'id': 1,
            'name': 'Johnson Corporation',
            'email': 'legal@johnsoncorp.com',
            'phone': '(555) 123-4567',
            'activeMatters': 3,
            'created': '2024-01-01'
        },
        {
            'id': 2,
            'name': 'TechStart Inc.',
            'email': 'ceo@techstart.com',
            'phone': '(555) 234-5678',
            'activeMatters': 2,
            'created': '2024-01-05'
        },
        {
            'id': 3,
            'name': 'Maria Rodriguez',
            'email': 'maria.r@email.com',
            'phone': '(555) 345-6789',
            'activeMatters': 1,
            'created': '2024-01-10'
        }
    ])
    
    # Sample matters
    matters_db.extend([
        {
            'id': 1,
            'title': 'Johnson vs. Smith Merger',
            'client': 'Johnson Corporation',
            'clientId': 1,
            'type': 'corporate',
            'status': 'active',
            'created': '2024-01-10',
            'value': '$2.5M',
            'description': 'Major corporate merger requiring regulatory approval and due diligence'
        },
        {
            'id': 2,
            'title': 'Real Estate Purchase - Downtown Office',
            'client': 'TechStart Inc.',
            'clientId': 2,
            'type': 'real-estate',
            'status': 'pending',
            'created': '2024-01-08',
            'value': '$850K',
            'description': 'Commercial real estate acquisition for expanding startup'
        },
        {
            'id': 3,
            'title': 'Employment Contract Dispute',
            'client': 'Maria Rodriguez',
            'clientId': 3,
            'type': 'litigation',
            'status': 'active',
            'created': '2024-01-05',
            'value': '$75K',
            'description': 'Non-compete clause enforcement and wrongful termination claims'
        }
    ])
    
    # Sample documents
    documents_db.extend([
        {
            'id': 1,
            'name': 'Merger Agreement v2.1',
            'type': 'contract',
            'status': 'final',
            'modified': '2024-01-15',
            'size': '2.3 MB',
            'description': 'Comprehensive merger agreement between Johnson Corp and Smith Industries',
            'matterId': 1,
            'filename': 'merger_agreement_v2.1.pdf'
        },
        {
            'id': 2,
            'name': 'Motion to Dismiss',
            'type': 'pleading',
            'status': 'review',
            'modified': '2024-01-14',
            'size': '1.8 MB',
            'description': 'Motion to dismiss for failure to state a claim',
            'matterId': 3,
            'filename': 'motion_to_dismiss.pdf'
        },
        {
            'id': 3,
            'name': 'Client Memo - Tax Implications',
            'type': 'memo',
            'status': 'draft',
            'modified': '2024-01-13',
            'size': '512 KB',
            'description': 'Analysis of tax implications for corporate restructuring',
            'matterId': 1,
            'filename': 'tax_memo.docx'
        }
    ])
    
    # Sample time entries
    time_entries_db.extend([
        {
            'id': 1,
            'matter': 'Johnson vs. Smith Merger',
            'matterId': 1,
            'date': '2024-01-15',
            'hours': 3.5,
            'rate': 250,
            'amount': 875.00,
            'description': 'Review merger documents and regulatory filing requirements',
            'attorney': 'John Doe'
        },
        {
            'id': 2,
            'matter': 'Real Estate Purchase',
            'matterId': 2,
            'date': '2024-01-14',
            'hours': 2.0,
            'rate': 250,
            'amount': 500.00,
            'description': 'Title search and purchase agreement review',
            'attorney': 'Jane Smith'
        },
        {
            'id': 3,
            'matter': 'Employment Dispute',
            'matterId': 3,
            'date': '2024-01-13',
            'hours': 1.5,
            'rate': 250,
            'amount': 375.00,
            'description': 'Client consultation and case strategy development',
            'attorney': 'John Doe'
        }
    ])

# Initialize sample data on startup
initialize_sample_data()

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_session():
    session_id = request.json.get('session_id') if request.is_json else request.form.get('session_id')
    if not session_id or session_id not in sessions_db:
        return None
    
    session_data = sessions_db[session_id]
    if datetime.now() > session_data['expires']:
        del sessions_db[session_id]
        return None
    
    return session_data

def create_session(user_data):
    session_id = str(uuid.uuid4())
    sessions_db[session_id] = {
        'user': user_data,
        'created': datetime.now(),
        'expires': datetime.now() + timedelta(hours=24)
    }
    return session_id

# Routes

# Serve the HTML frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'index.html')

# Serve static files (CSS, JS, images)
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# Authentication endpoints
@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        # Check if user exists (in production, verify password hash)
        if email in users_db:
            user_data = users_db[email]
            if check_password_hash(user_data['password_hash'], password):
                session_id = create_session({
                    'email': email,
                    'firmName': user_data['firmName'],
                    'role': user_data['role']
                })
                return jsonify({
                    'session_id': session_id,
                    'user': {
                        'email': email,
                        'firmName': user_data['firmName'],
                        'role': user_data['role']
                    }
                })
            else:
                return jsonify({'error': 'Invalid credentials'}), 401
        else:
            # For demo purposes, auto-create user
            user_data = {
                'email': email,
                'firmName': 'Demo Law Firm',
                'role': 'Partner',
                'password_hash': generate_password_hash(password)
            }
            users_db[email] = user_data
            
            session_id = create_session({
                'email': email,
                'firmName': user_data['firmName'],
                'role': user_data['role']
            })
            
            return jsonify({
                'session_id': session_id,
                'user': {
                    'email': email,
                    'firmName': user_data['firmName'],
                    'role': user_data['role']
                }
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        firm_name = data.get('firmName', 'Law Firm')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        if email in users_db:
            return jsonify({'error': 'User already exists'}), 409
        
        # Create new user
        user_data = {
            'email': email,
            'firmName': firm_name,
            'role': 'Partner',
            'password_hash': generate_password_hash(password),
            'created': datetime.now().isoformat()
        }
        users_db[email] = user_data
        
        session_id = create_session({
            'email': email,
            'firmName': firm_name,
            'role': 'Partner'
        })
        
        return jsonify({
            'session_id': session_id,
            'user': {
                'email': email,
                'firmName': firm_name,
                'role': 'Partner'
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    try:
        data = request.json
        session_id = data.get('session_id')
        
        if session_id and session_id in sessions_db:
            del sessions_db[session_id]
        
        return jsonify({'message': 'Logged out successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/validate', methods=['POST'])
def validate_session_endpoint():
    session_data = validate_session()
    if session_data:
        return jsonify({
            'valid': True,
            'user': session_data['user']
        })
    else:
        return jsonify({'valid': False}), 401

# Document endpoints
@app.route('/api/documents', methods=['GET'])
def get_documents():
    session_data = validate_session()
    if not session_data:
        return jsonify({'error': 'Invalid session'}), 401
    
    # Get query parameters for filtering
    search = request.args.get('search', '')
    doc_type = request.args.get('type', '')
    
    filtered_docs = documents_db.copy()
    
    if search:
        filtered_docs = [doc for doc in filtered_docs 
                        if search.lower() in doc['name'].lower() 
                        or search.lower() in doc['description'].lower()]
    
    if doc_type:
        filtered_docs = [doc for doc in filtered_docs if doc['type'] == doc_type]
    
    return jsonify(filtered_docs)

@app.route('/api/documents/upload', methods=['POST'])
def upload_document():
    session_data = validate_session()
    if not session_data:
        return jsonify({'error': 'Invalid session'}), 401
    
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Get form data
            name = request.form.get('name', filename.rsplit('.', 1)[0])
            doc_type = request.form.get('type', 'document')
            matter_id = request.form.get('matter')
            description = request.form.get('description', 'Uploaded document')
            
            # Create document record
            new_doc = {
                'id': len(documents_db) + 1,
                'name': name,
                'type': doc_type,
                'status': 'review',
                'modified': datetime.now().strftime('%Y-%m-%d'),
                'size': f'{os.path.getsize(file_path) / 1024 / 1024:.1f} MB',
                'description': description,
                'filename': filename,
                'matterId': int(matter_id) if matter_id else None
            }
            
            documents_db.append(new_doc)
            
            return jsonify({
                'message': 'Document uploaded successfully',
                'document': new_doc
            })
        else:
            return jsonify({'error': 'File type not allowed'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Matter endpoints
@app.route('/api/matters', methods=['GET'])
def get_matters():
    session_data = validate_session()
    if not session_data:
        return jsonify({'error': 'Invalid session'}), 401
    
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    
    filtered_matters = matters_db.copy()
    
    if search:
        filtered_matters = [matter for matter in filtered_matters 
                           if search.lower() in matter['title'].lower() 
                           or search.lower() in matter['client'].lower()]
    
    if status:
        filtered_matters = [matter for matter in filtered_matters if matter['status'] == status]
    
    return jsonify(filtered_matters)

@app.route('/api/matters', methods=['POST'])
def create_matter():
    session_data = validate_session()
    if not session_data:
        return jsonify({'error': 'Invalid session'}), 401
    
    try:
        data = request.json
        
        # Find client name
        client_id = int(data.get('client'))
        client = next((c for c in clients_db if c['id'] == client_id), None)
        client_name = client['name'] if client else 'Unknown Client'
        
        new_matter = {
            'id': len(matters_db) + 1,
            'title': data['title'],
            'client': client_name,
            'clientId': client_id,
            'type': data['type'],
            'status': 'active',
            'created': datetime.now().strftime('%Y-%m-%d'),
            'value': '$0',
            'description': data.get('description', '')
        }
        
        matters_db.append(new_matter)
        
        return jsonify({
            'message': 'Matter created successfully',
            'matter': new_matter
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Client endpoints
@app.route('/api/clients', methods=['GET'])
def get_clients():
    session_data = validate_session()
    if not session_data:
        return jsonify({'error': 'Invalid session'}), 401
    
    return jsonify(clients_db)

# Time & Billing endpoints
@app.route('/api/time-entries', methods=['GET'])
def get_time_entries():
    session_data = validate_session()
    if not session_data:
        return jsonify({'error': 'Invalid session'}), 401
    
    return jsonify(time_entries_db)

@app.route('/api/time-entries', methods=['POST'])
def add_time_entry():
    session_data = validate_session()
    if not session_data:
        return jsonify({'error': 'Invalid session'}), 401
    
    try:
        data = request.json
        
        matter_id = int(data['matter'])
        matter = next((m for m in matters_db if m['id'] == matter_id), None)
        matter_title = matter['title'] if matter else 'Unknown Matter'
        
        hours = float(data['hours'])
        rate = 250  # Default hourly rate
        amount = hours * rate
        
        new_entry = {
            'id': len(time_entries_db) + 1,
            'matter': matter_title,
            'matterId': matter_id,
            'date': data['date'],
            'hours': hours,
            'rate': rate,
            'amount': amount,
            'description': data['description'],
            'attorney': session_data['user']['email']
        }
        
        time_entries_db.append(new_entry)
        
        return jsonify({
            'message': 'Time entry added successfully',
            'entry': new_entry
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Dashboard endpoints
@app.route('/api/dashboard/metrics', methods=['GET'])
def get_dashboard_metrics():
    session_data = validate_session()
    if not session_data:
        return jsonify({'error': 'Invalid session'}), 401
    
    active_matters = len([m for m in matters_db if m['status'] == 'active'])
    total_documents = len(documents_db)
    active_clients = len(clients_db)
    total_hours = sum(entry['hours'] for entry in time_entries_db)
    
    return jsonify({
        'activeMatters': active_matters,
        'totalDocuments': total_documents,
        'activeClients': active_clients,
        'billableHours': total_hours
    })

@app.route('/api/dashboard/activity', methods=['GET'])
def get_recent_activity():
    session_data = validate_session()
    if not session_data:
        return jsonify({'error': 'Invalid session'}), 401
    
    # Generate recent activity from recent documents and matters
    activity = []
    
    # Recent documents
    for doc in sorted(documents_db, key=lambda x: x['modified'], reverse=True)[:3]:
        activity.append({
            'id': f"doc_{doc['id']}",
            'title': f"Document: {doc['name']}",
            'description': doc['description'],
            'status': doc['status'],
            'date': doc['modified'],
            'user': session_data['user']['email']
        })
    
    return jsonify(activity)

# Search endpoint
@app.route('/api/search', methods=['POST'])
def search():
    session_data = validate_session()
    if not session_data:
        return jsonify({'error': 'Invalid session'}), 401
    
    try:
        data = request.json
        query = data.get('query', '').lower()
        content_type = data.get('contentType', '')
        
        results = []
        
        if not content_type or content_type == 'documents':
            for doc in documents_db:
                if query in doc['name'].lower() or query in doc['description'].lower():
                    results.append({
                        'id': f"doc_{doc['id']}",
                        'title': doc['name'],
                        'type': 'Document',
                        'date': doc['modified'],
                        'excerpt': f"Found in document: {doc['description'][:100]}..."
                    })
        
        if not content_type or content_type == 'matters':
            for matter in matters_db:
                if query in matter['title'].lower() or query in matter['description'].lower():
                    results.append({
                        'id': f"matter_{matter['id']}",
                        'title': matter['title'],
                        'type': 'Matter',
                        'date': matter['created'],
                        'excerpt': f"Found in matter: {matter['description'][:100]}..."
                    })
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large'}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("Starting LegalDoc Pro API Server...")
    print("Frontend available at: http://localhost:5000")
    print("API endpoints available at: http://localhost:5000/api/*")
    app.run(debug=True, host='0.0.0.0', port=5000)
