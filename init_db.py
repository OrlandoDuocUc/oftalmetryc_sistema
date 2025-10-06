import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# Cargar variables de entorno para obtener la URL de la base de datos
load_dotenv()
print("🔧 Cargando variables de entorno para inicialización...")

# Importar el 'engine' y la 'Base' directamente, y todos los modelos
from app.infraestructure.utils.db import engine, SessionLocal
from app.infraestructure.utils.tables import Base
from app.domain.models.user import User
from app.domain.models.rol import Rol
from app.domain.models.products import Product
from app.domain.models.sale import Sale
from app.domain.models.cliente import Cliente
from app.domain.models.proveedor import Proveedor
# ... (añade aquí CUALQUIER otro modelo que hayas creado) ...

def initialize_database():
    """
    Esta función se conecta a la base de datos usando el 'engine' de SQLAlchemy,
    borra las tablas existentes y las vuelve a crear usando los metadatos de 'Base'.
    Luego, inserta los datos iniciales.
    """
    print("Conectando a la base de datos para inicialización...")
    try:
        # La forma correcta de crear tablas con tu configuración de modelos
        print("Borrando tablas existentes (si las hay)...")
        Base.metadata.drop_all(bind=engine)
        print("Creando todas las tablas nuevas...")
        Base.metadata.create_all(bind=engine)
        
    except Exception as e:
        print(f"❌ ERROR CRÍTICO durante la creación de tablas: {e}")
        # Si la creación de tablas falla, no tiene sentido continuar.
        return

    # --- INSERTAR DATOS INICIALES ESENCIALES ---
    session = SessionLocal()
    try:
        # Crear Roles
        print("Creando roles 'Administrador' y 'Vendedor'...")
        rol_admin = Rol(nombre='Administrador', descripcion='Acceso total al sistema')
        rol_vendedor = Rol(nombre='Vendedor', descripcion='Acceso al punto de venta')
        session.add(rol_admin)
        session.add(rol_vendedor)
        session.commit() # Guardamos los roles para obtener sus IDs

        # Crear Usuario Administrador por defecto
        print("Creando usuario 'admin' por defecto...")
        admin_password_hash = generate_password_hash('admin123') # Cambia esta contraseña si quieres
        admin_user = User(
            nombre='Admin',
            ap_pat='Sistema',
            ap_mat='',
            username='admin',
            email='admin@oftalmetryc.cl',
            password=admin_password_hash,
            rol_id=rol_admin.rol_id, # Asignar el ID del rol recién creado
            estado=True
        )
        session.add(admin_user)
        session.commit()
        
        print("✅ ¡Base de datos inicializada y datos esenciales creados con éxito!")
        
    except Exception as e:
        print(f"❌ Error durante la inserción de datos iniciales: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    # Esto permite que el script se ejecute directamente desde la terminal
    initialize_database()

