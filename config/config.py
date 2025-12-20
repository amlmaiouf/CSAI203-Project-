import os

class Config:
    """Base Configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_secret_key'
    DEBUG = False
    TESTING = False
    # Database Settings (adapted for your SQL Server)
    DB_DRIVER = '{SQL Server}'
    DB_SERVER = 'MSI\\SQLEXPRESS'
    DB_DATABASE = 'elderly_care_system'
    DB_TRUSTED_CONNECTION = 'yes'

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'
    # In production, we might use a username/password instead of Trusted_Connection
    
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}