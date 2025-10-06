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
        
        # Agregar parámetros de encoding si no existen
        if 'client_encoding' not in DATABASE_URL and 'localhost' in DATABASE_URL:
            DATABASE_URL += '?client_encoding=utf8'
            print("🔤 [BaseConfig] Agregado client_encoding=utf8 para localhost")
        
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
        print(f"🗄️ [BaseConfig] Usando DATABASE_URL: {DATABASE_URL[:50]}...")
    else:
        # Construir URL usando credenciales individuales como fallback
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', '12345')
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'optica_db')
        
        SQLALCHEMY_DATABASE_URI = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?client_encoding=utf8'
        print(f"🏠 [BaseConfig] Construyendo URL local: postgresql://{db_user}:***@{db_host}:{db_port}/{db_name}")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {
            'client_encoding': 'utf8',
            'application_name': 'optica_maipu_app',
            'options': '-c client_encoding=utf8'
        },
        'echo': False,
        'isolation_level': 'AUTOCOMMIT'
    }

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
