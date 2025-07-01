# AWS Lambda WSGI Handler
# File: wsgi_handler.py

try:
    import unzip_requirements
except ImportError:
    pass

import serverless_wsgi
from app import app

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
