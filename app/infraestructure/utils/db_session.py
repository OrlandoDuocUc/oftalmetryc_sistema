from app.infraestructure.utils.db import SessionLocal

def get_db_session():
    """Obtiene una sesión de base de datos"""
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        db.close()
        raise e

def close_db_session(db):
    """Cierra una sesión de base de datos"""
    if db:
        db.close() 