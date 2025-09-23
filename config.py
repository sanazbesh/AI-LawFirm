import os
from datetime import datetime

def load_config():
    return {
        "app_name": "LegalDoc Pro",
        "version": "2.0.0",
        "debug": os.getenv("DEBUG", "False").lower() == "true",
        "port": int(os.getenv("PORT", "5001")),
        "timezone": "America/New_York",
        "max_file_size": 50 * 1024 * 1024,  # 50MB
        "allowed_file_types": [".pdf", ".docx", ".txt", ".png", ".jpg"],
        "default_billing_rates": {
            "partner": 500.0,
            "senior_associate": 350.0,
            "associate": 250.0,
            "paralegal": 150.0
        }
    }
