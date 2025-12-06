import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'elderly-care-secret-key-2024'
    
    # SQL Server Express Connection
    SQLALCHEMY_DATABASE_URI = (
        'mssql+pyodbc://localhost\\SQLEXPRESS/elderly_care_system'
        '?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    SESSION_TYPE = 'filesystem'