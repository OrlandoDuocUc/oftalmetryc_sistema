# app/infraestructure/utils/db.py

import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

# Instancia global de Flask-SQLAlchemy usada por los blueprints/controladores
# Desactivamos autoflush/expire para evitar sorpresas entre requests
db = SQLAlchemy(session_options={"autoflush": False, "expire_on_commit": False})

# CONFIGURACIÓN CORREGIDA PARA RENDER
# Priorizar DATABASE_URL completa de Render
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Normaliza esquema de URI antigua de Heroku si hiciera falta
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    print(f"🔗 [db.py] Usando DATABASE_URL de Render: {DATABASE_URL[:50]}...")
else:
    # Fallback para desarrollo local
    print("🏠 [db.py] Usando configuración local")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "12345")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "optica_db")

    # Escapar caracteres especiales en la contraseña
    password_encoded = quote_plus(DB_PASSWORD)

    # URL de conexión PostgreSQL con encoding explícito
    DATABASE_URL = (
        f"postgresql://{DB_USER}:{password_encoded}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        f"?client_encoding=utf8&application_name=optica_app"
    )
    print(f"🔧 [db.py] URL local construida: {DATABASE_URL}")

# Engine "clásico" (mantengo porque tu dominio podría usarlo)
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    connect_args={
        "client_encoding": "utf8",
        "application_name": "optica_maipu_app",
    },
)

# Session factory "clásica" (para repositorios/UseCases que la usen)
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

def get_connection():
    """Obtiene una conexión directa a la base de datos (psycopg2)."""
    import psycopg2
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"❌ Error conectando a BD: {e}")
        return None

def get_session():
    """Obtiene una sesión de SQLAlchemy (clásica)."""
    return SessionLocal()
