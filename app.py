"""
Elderly Care System - Main Application Entry Point
FR15: Admin Service Management
Following MVC Architecture Pattern
"""

from flask import Flask
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
