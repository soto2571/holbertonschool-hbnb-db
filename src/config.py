"""
Configuration settings for the application.
"""

import os


class Config:
    """Configuration base class"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USE_DATABASE = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
    DEBUG = True
    USE_DATABASE = True


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///test.db')
    DEBUG = True
    TESTING = True
    USE_DATABASE = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///prod.db')
    DEBUG = False
    USE_DATABASE = True


config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig
)

key = Config.SECRET_KEY
