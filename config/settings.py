import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class BaseConfig:
    DEBUG = False
    TESTING = False
    JSON_SORT_KEYS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Configuración de base de datos
    DATABASE_URL = os.getenv('DATABASE_URL')
    print(f"⚙️ [BaseConfig] DATABASE_URL detectada: {'Sí' if DATABASE_URL else 'No'}")
    
    if DATABASE_URL:
        # Convertir postgres:// a postgresql:// si es necesario
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
            print("🔄 [BaseConfig] Convertido postgres:// a postgresql://")
        
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
        print(f"🗄️ [BaseConfig] Usando DATABASE_URL: {DATABASE_URL[:50]}...")
    else:
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432/optica_db'
        print("🏠 [BaseConfig] Usando base de datos local por defecto")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENV = 'development'

class ProductionConfig(BaseConfig):
    ENV = 'production'
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY", "production-secret-key") 

class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True
    ENV = 'testing'

config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
