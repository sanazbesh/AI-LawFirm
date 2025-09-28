from dotenv import load_dotenv
load_dotenv()  # This loads .env file variables
import os
import uuid
import boto3
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_migrate import Migrate
import redis
from sqlalchemy.exc import IntegrityError

# Initialize Flask app
app = Flask(__name__)

# Configuration from environment variables
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///legaldoc_pro.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# File upload configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'doc', 'xlsx', 'pptx'}

# AWS S3 Configuration (optional)
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
S3_BUCKET = os.environ.get('S3_BUCKET_NAME')
USE_S3 = all([AWS_ACCESS_KEY, AWS_SECRET_KEY, S3_BUCKET])

if USE_S3:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

# Redis configuration (for sessions/caching)
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
try:
    redis_client = redis.from_url(REDIS_URL)
    redis_client.ping()  # Test connection
    USE_REDIS = True
except:
    USE_REDIS = False
    print("Redis not available, using in-memory storage")

# Initialize extensions
CORS(app, supports_credentials=True)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Database Models
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    firm_name = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='Partner')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    matters = db.relationship('Matter', backref='assigned_user', lazy=True)
    time_entries = db.relationship('TimeEntry', backref='attorney_user', lazy=True)

class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    matters = db.relationship('Matter', backref='client_info', lazy=True)

class Matter(db.Model):
    __tablename__ = 'matters'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text)
    matter_type = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='active')
    estimated_value = db.Column(db.Numeric(12, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    assigned_attorney_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    documents = db.relationship('Document', backref='related_matter', lazy=True)
    time_entries = db.relationship('TimeEntry', backref='related_matter', lazy=True)

class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text)
    document_type = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='draft')
    file_path = db.Column(db.String(500))  # S3 URL or local path
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    matter_id = db.Column(db.Integer, db.ForeignKey('matters.id'))
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class TimeEntry(db.Model):
    __tablename__ = 'time_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    hours = db.Column(db.Numeric(5, 2), nullable=False)
    hourly_rate = db.Column(db.Numeric(8, 2), nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    entry_date = db.Column(db.Date, nullable=False)
    is_billable = db.Column(db.Boolean, default=True)
    is_billed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    matter_id = db.Column(db.Integer, db.ForeignKey('matters.id'), nullable=False)
    attorney_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100), nullable=False)
    resource_type = db.Column(db.String(50))
    resource_id = db.Column(db.Integer)
    details = db.Column(db.JSON)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Helper Functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_to_s3(file, filename):
    """Upload file to S3 and return the URL"""
    if not USE_S3:
        return None
    
    try:
        s3_client.upload_fileobj(
            file,
            S3_BUCKET,
            filename,
            ExtraArgs={"ACL": "private"}
        )
        return f"https://{S3_BUCKET}.s3.amazonaws.com/{filename}"
    except Exception as e:
        print(f"S3 upload error: {e}")
        return None

def save_file_locally(file, filename):
    """Save file locally and return the path"""
    upload_folder = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    return file_path

def log_audit_event(user_id, action, resource_type=None, resource_id=None, details=None):
    """Log audit events"""
    try:
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(audit_log)
        db.session.commit()
    except Exception as e:
        print(f"Audit log error: {e}")

# Routes

# Serve Frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# Authentication Routes
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        email = data.get('email', '').lower().strip()
        password = data.get('password', '')
        firm_name = data.get('firmName', '').strip()
        
        if not all([email, password, firm_name]):
            return jsonify({'error': 'Email, password, and firm name are required'}), 400
        
        if len(password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters'}), 400
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'User already exists'}), 409
        
        # Create new user
        password_hash = generate_password_hash(password)
        new_user = User(
            email=email,
            password_hash=password_hash,
            firm_name=firm_name
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Generate JWT token
        access_token = create_access_token(identity=new_user.id)
        
        # Log audit event
        log_audit_event(new_user.id, 'USER_SIGNUP')
        
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': new_user.id,
                'email': new_user.email,
                'firmName': new_user.firm_name,
                'role': new_user.role
            }
        }), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'User already exists'}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email', '').lower().strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        user = User.query.filter_by(email=email, is_active=True).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Generate JWT token
        access_token = create_access_token(identity=user.id)
        
        # Log audit event
        log_audit_event(user.id, 'USER_LOGIN')
        
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'firmName': user.firm_name,
                'role': user.role
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/validate', methods=['POST'])
@jwt_required()
def validate_token():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({'valid': False}), 401
        
        return jsonify({
            'valid': True,
            'user': {
                'id': user.id,
                'email': user.email,
                'firmName': user.firm_name,
                'role': user.role
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Client Routes
@app.route('/api/clients', methods=['GET'])
@jwt_required()
def get_clients():
    try:
        clients = Client.query.filter_by(is_active=True).all()
        return jsonify([{
            'id': client.id,
            'name': client.name,
            'email': client.email,
            'phone': client.phone,
            'activeMatters': len([m for m in client.matters if m.status == 'active'])
        } for client in clients])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clients', methods=['POST'])
@jwt_required()
def create_client():
    try:
        current_user_id = get_jwt_identity()
        data = request.json
        
        new_client = Client(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone', ''),
            address=data.get('address', '')
        )
        
        db.session.add(new_client)
        db.session.commit()
        
        log_audit_event(current_user_id, 'CLIENT_CREATED', 'client', new_client.id)
        
        return jsonify({
            'message': 'Client created successfully',
            'client': {
                'id': new_client.id,
                'name': new_client.name,
                'email': new_client.email,
                'phone': new_client.phone
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Matter Routes
@app.route('/api/matters', methods=['GET'])
@jwt_required()
def get_matters():
    try:
        search = request.args.get('search', '')
        status = request.args.get('status', '')
        
        query = Matter.query.join(Client)
        
        if search:
            query = query.filter(
                db.or_(
                    Matter.title.ilike(f'%{search}%'),
                    Client.name.ilike(f'%{search}%')
                )
            )
        
        if status:
            query = query.filter(Matter.status == status)
        
        matters = query.all()
        
        return jsonify([{
            'id': matter.id,
            'title': matter.title,
            'client': matter.client_info.name,
            'clientId': matter.client_id,
            'type': matter.matter_type,
            'status': matter.status,
            'created': matter.created_at.strftime('%Y-%m-%d'),
            'value': f'${matter.estimated_value or 0:,.2f}',
            'description': matter.description or ''
        } for matter in matters])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/matters', methods=['POST'])
@jwt_required()
def create_matter():
    try:
        current_user_id = get_jwt_identity()
        data = request.json
        
        new_matter = Matter(
            title=data.get('title'),
            description=data.get('description', ''),
            matter_type=data.get('type'),
            client_id=data.get('client'),
            assigned_attorney_id=current_user_id,
            estimated_value=data.get('value', 0)
        )
        
        db.session.add(new_matter)
        db.session.commit()
        
        log_audit_event(current_user_id, 'MATTER_CREATED', 'matter', new_matter.id)
        
        return jsonify({
            'message': 'Matter created successfully',
            'matter': {
                'id': new_matter.id,
                'title': new_matter.title,
                'client': new_matter.client_info.name,
                'type': new_matter.matter_type,
                'status': new_matter.status
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Document Routes
@app.route('/api/documents', methods=['GET'])
@jwt_required()
def get_documents():
    try:
        search = request.args.get('search', '')
        doc_type = request.args.get('type', '')
        
        query = Document.query
        
        if search:
            query = query.filter(
                db.or_(
                    Document.name.ilike(f'%{search}%'),
                    Document.description.ilike(f'%{search}%')
                )
            )
        
        if doc_type:
            query = query.filter(Document.document_type == doc_type)
        
        documents = query.order_by(Document.created_at.desc()).all()
        
        return jsonify([{
            'id': doc.id,
            'name': doc.name,
            'type': doc.document_type,
            'status': doc.status,
            'modified': doc.updated_at.strftime('%Y-%m-%d'),
            'size': f'{doc.file_size / 1024 / 1024:.1f} MB' if doc.file_size else 'Unknown',
            'description': doc.description or '',
            'matterId': doc.matter_id
        } for doc in documents])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/documents/upload', methods=['POST'])
@jwt_required()
def upload_document():
    try:
        current_user_id = get_jwt_identity()
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        # Generate secure filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        
        # Upload file
        if USE_S3:
            file_url = upload_file_to_s3(file, unique_filename)
            if not file_url:
                return jsonify({'error': 'File upload failed'}), 500
            file_path = file_url
        else:
            file_path = save_file_locally(file, unique_filename)
        
        # Create document record
        new_document = Document(
            name=request.form.get('name', filename.rsplit('.', 1)[0]),
            description=request.form.get('description', ''),
            document_type=request.form.get('type', 'document'),
            file_path=file_path,
            file_size=len(file.read()),
            mime_type=file.content_type,
            matter_id=request.form.get('matter') if request.form.get('matter') else None,
            uploaded_by_id=current_user_id
        )
        
        # Reset file pointer after reading size
        file.seek(0)
        
        db.session.add(new_document)
        db.session.commit()
        
        log_audit_event(current_user_id, 'DOCUMENT_UPLOADED', 'document', new_document.id)
        
        return jsonify({
            'message': 'Document uploaded successfully',
            'document': {
                'id': new_document.id,
                'name': new_document.name,
                'type': new_document.document_type,
                'status': new_document.status
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Time Entry Routes
@app.route('/api/time-entries', methods=['GET'])
@jwt_required()
def get_time_entries():
    try:
        current_user_id = get_jwt_identity()
        
        entries = TimeEntry.query\
            .filter_by(attorney_id=current_user_id)\
            .join(Matter)\
            .order_by(TimeEntry.entry_date.desc())\
            .all()
        
        return jsonify([{
            'id': entry.id,
            'matter': entry.related_matter.title,
            'matterId': entry.matter_id,
            'date': entry.entry_date.strftime('%Y-%m-%d'),
            'hours': float(entry.hours),
            'amount': f'${float(entry.total_amount):,.2f}',
            'description': entry.description
        } for entry in entries])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/time-entries', methods=['POST'])
@jwt_required()
def add_time_entry():
    try:
        current_user_id = get_jwt_identity()
        data = request.json
        
        hours = float(data.get('hours', 0))
        rate = float(data.get('rate', 250))  # Default $250/hour
        total_amount = hours * rate
        
        new_entry = TimeEntry(
            description=data.get('description'),
            hours=hours,
            hourly_rate=rate,
            total_amount=total_amount,
            entry_date=datetime.strptime(data.get('date'), '%Y-%m-%d').date(),
            matter_id=data.get('matter'),
            attorney_id=current_user_id
        )
        
        db.session.add(new_entry)
        db.session.commit()
        
        log_audit_event(current_user_id, 'TIME_ENTRY_CREATED', 'time_entry', new_entry.id)
        
        return jsonify({
            'message': 'Time entry added successfully',
            'entry': {
                'id': new_entry.id,
                'hours': float(new_entry.hours),
                'amount': f'${float(new_entry.total_amount):,.2f}',
                'matter': new_entry.related_matter.title
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Dashboard Routes
@app.route('/api/dashboard/metrics', methods=['GET'])
@jwt_required()
def get_dashboard_metrics():
    try:
        active_matters = Matter.query.filter_by(status='active').count()
        total_documents = Document.query.count()
        active_clients = Client.query.filter_by(is_active=True).count()
        
        total_hours_result = db.session.query(db.func.sum(TimeEntry.hours)).scalar()
        total_hours = float(total_hours_result) if total_hours_result else 0
        
        return jsonify({
            'activeMatters': active_matters,
            'totalDocuments': total_documents,
            'activeClients': active_clients,
            'billableHours': total_hours
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Search Route
@app.route('/api/search', methods=['POST'])
@jwt_required()
def search():
    try:
        data = request.json
        query = data.get('query', '').strip()
        content_type = data.get('contentType', '')
        
        if not query:
            return jsonify([])
        
        results = []
        
        # Search documents
        if not content_type or content_type == 'documents':
            documents = Document.query.filter(
                db.or_(
                    Document.name.ilike(f'%{query}%'),
                    Document.description.ilike(f'%{query}%')
                )
            ).limit(10).all()
            
            for doc in documents:
                results.append({
                    'id': f"doc_{doc.id}",
                    'title': doc.name,
                    'type': 'Document',
                    'date': doc.created_at.strftime('%Y-%m-%d'),
                    'excerpt': f"Document: {doc.description[:100]}..." if doc.description else doc.name
                })
        
        # Search matters
        if not content_type or content_type == 'matters':
            matters = Matter.query.filter(
                db.or_(
                    Matter.title.ilike(f'%{query}%'),
                    Matter.description.ilike(f'%{query}%')
                )
            ).limit(10).all()
            
            for matter in matters:
                results.append({
                    'id': f"matter_{matter.id}",
                    'title': matter.title,
                    'type': 'Matter',
                    'date': matter.created_at.strftime('%Y-%m-%d'),
                    'excerpt': f"Matter: {matter.description[:100]}..." if matter.description else matter.title
                })
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error Handlers
@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large'}), 413

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

# Initialize Database
# Initialize Database
def create_tables():
    with app.app_context():
        db.create_all()
        
        # Create sample data if no users exist
        if User.query.count() == 0:
            print("Creating sample data...")
            
            # Create sample user
            sample_user = User(
                email='admin@legaldocpro.com',
                password_hash=generate_password_hash('admin123'),
                firm_name='LegalDoc Pro Firm',
                role='Senior Partner'
            )
            db.session.add(sample_user)
            
            # Create sample clients
            clients_data = [
                {'name': 'Johnson Corporation', 'email': 'legal@johnsoncorp.com', 'phone': '(555) 123-4567'},
                {'name': 'TechStart Inc.', 'email': 'ceo@techstart.com', 'phone': '(555) 234-5678'},
                {'name': 'Maria Rodriguez', 'email': 'maria.r@email.com', 'phone': '(555) 345-6789'}
            ]
            
            for client_data in clients_data:
                client = Client(**client_data)
                db.session.add(client)
            
            db.session.commit()
            print("Sample data created successfully!")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    # Initialize database tables
    create_tables()
    
    print("Starting LegalDoc Pro Production Server...")
    print(f"Frontend available at: http://localhost:{port}")
    print(f"API endpoints available at: http://localhost:{port}/api/*")
    print(f"Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Redis: {'Enabled' if USE_REDIS else 'Disabled'}")
    print(f"S3 Storage: {'Enabled' if USE_S3 else 'Disabled (using local storage)'}")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
