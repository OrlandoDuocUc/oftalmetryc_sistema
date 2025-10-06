from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from urllib.parse import quote_plus

# CONFIGURACIÓN CORREGIDA PARA RENDER
# Priorizar DATABASE_URL completa de Render
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    # Si tenemos DATABASE_URL (Render), usarla directamente
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    print(f"🔗 [db.py] Usando DATABASE_URL de Render: {DATABASE_URL[:50]}...")
else:
    # Fallback para desarrollo local
    print("🏠 [db.py] Usando configuración local")
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '12345')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'optica_db')
    
    # Escapar caracteres especiales en la contraseña
    password_encoded = quote_plus(DB_PASSWORD)
    
    # URL de conexión PostgreSQL con encoding explícito
    DATABASE_URL = f"postgresql://{DB_USER}:{password_encoded}@{DB_HOST}:{DB_PORT}/{DB_NAME}?client_encoding=utf8&application_name=optica_app"
    print(f"🔧 [db.py] URL local construida: {DATABASE_URL}")

# Configuración anterior SQL Server (comentada)
# DATABASE_URL = (
#     "mssql+pyodbc://adminbd:Admin2025@proyectobd.database.windows.net:1433"
#     "/?database=optica-maipu&driver=ODBC+Driver+17+for+SQL+Server"
# )

engine = create_engine(
    DATABASE_URL, 
    echo=True,  # Activar logs para debug
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verificar conexiones antes de usar
    connect_args={
        "client_encoding": "utf8",
        "application_name": "optica_maipu_app"
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

def get_connection():
    """Obtiene una conexión directa a la base de datos"""
    import psycopg2
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"❌ Error conectando a BD: {e}")
        return None

def get_session():
    """Obtiene una sesión de SQLAlchemy"""
    return SessionLocal()
