import os


class Config:
    """Configuração padrão"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')  # Exemplo de banco em produção
    SECRET_KEY = 'sua-chave-secreta'


class DevelopmentConfig(Config):
    """Configuração para desenvolvimento"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'


class TestingConfig(Config):
    """Configuração para testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Banco de dados em memória (temporário)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
