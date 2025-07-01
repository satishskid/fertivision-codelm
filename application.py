# AWS Elastic Beanstalk Application Entry Point
# File: application.py

from app import app

# AWS Elastic Beanstalk expects the application to be called 'application'
application = app

if __name__ == "__main__":
    application.run(debug=False, host='0.0.0.0', port=8000)
