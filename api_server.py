from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys

# Add your existing modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Serve the HTML file
@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'index.html')

# Authentication endpoints
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    # Integrate with your existing auth service
    return jsonify({
        'session_id': 'demo_session_123',
        'user': {
            'email': data['email'],
            'firmName': 'Demo Law Firm',
            'role': 'Partner'
        }
    })

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    data = request.json
    return jsonify({
        'session_id': 'new_session_456',
        'user': {
            'email': data['email'],
            'firmName': data['firmName'],
            'role': 'Partner'
        }
    })

# Document endpoints
@app.route('/api/documents', methods=['GET'])
def get_documents():
    # Connect to your existing document management
    return jsonify([
        # Your existing document data
    ])

@app.route('/api/documents/upload', methods=['POST'])
def upload_document():
    # Handle file upload using your existing services
    return jsonify({'success': True, 'message': 'Document uploaded'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
