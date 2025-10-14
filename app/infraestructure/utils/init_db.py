import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()
print("🔄 Cargando variables de entorno para inicialización...")

from app.infraestructure.utils.db import engine, SessionLocal
from app.infraestructure.utils.tables import Base
from app.domain.models.user import User
from app.domain.models.rol import Rol
from app.domain.models.products import Product
from app.domain.models.sale import Sale
from app.domain.models.cliente import Cliente
from app.domain.models.proveedor import Proveedor

_ALLOWED_RESET_VALUES = {"1", "true", "yes", "on"}

def _can_reset_database() -> bool:
    env = os.getenv("FLASK_ENV", "development").lower()
    allow_flag = os.getenv("ALLOW_DB_RESET", "").strip().lower()
    if env in ("development", "local"):
        return True
    if allow_flag in _ALLOWED_RESET_VALUES:
        return True
    return False

def initialize_database():
    if not _can_reset_database():
        print("⚠️  init_db: ejecución bloqueada. Estás en un entorno protegido o falta ALLOW_DB_RESET.")
        print("    Si realmente necesitas reinicializar, ejecuta export ALLOW_DB_RESET=true (o variable equivalente) y vuelve a intentarlo.")
        return

    print("Conectando a la base de datos para inicialización...")
    try:
        print("Borrando tablas existentes (si las hay)...")
        Base.metadata.drop_all(bind=engine)
        print("Creando todas las tablas nuevas...")
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"❌ ERROR CRÍTICO durante la creación de tablas: {e}")
        return

    session = SessionLocal()
    try:
        print("Creando roles 'Administrador' y 'Vendedor'...")
        rol_admin = Rol(nombre='Administrador', descripcion='Acceso total al sistema')
        rol_vendedor = Rol(nombre='Vendedor', descripcion='Acceso al punto de venta')
        session.add_all([rol_admin, rol_vendedor])
        session.commit()

        print("Creando usuario 'admin' por defecto...")
        admin_password_hash = generate_password_hash('admin123')
        admin_user = User(
            nombre='Admin',
            ap_pat='Sistema',
            ap_mat='',
            username='admin',
            email='admin@oftalmetryc.cl',
            password=admin_password_hash,
            rol_id=rol_admin.rol_id,
            estado=True
        )
        session.add(admin_user)
        session.commit()

        print("✅ Base de datos inicializada y datos esenciales creados con éxito.")
    except Exception as e:
        print(f"❌ Error durante la inserción de datos iniciales: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    initialize_database()
