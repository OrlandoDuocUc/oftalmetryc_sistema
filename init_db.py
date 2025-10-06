import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# Cargar variables de entorno para obtener la URL de la base de datos
load_dotenv()
print("🔧 Cargando variables de entorno para inicialización...")

# Importar la configuración de la base de datos y TODOS los modelos
from app.infraestructure.utils.db import db, SessionLocal
from app.domain.models.user import User
from app.domain.models.rol import Rol
from app.domain.models.products import Product
from app.domain.models.sale import Sale
from app.domain.models.cliente import Cliente
from app.domain.models.proveedor import Proveedor
# ... (si tienes más modelos, añádelos aquí) ...
# Por ejemplo: from app.domain.models.paciente import Paciente

def initialize_database():
    """
    Esta función se conecta a la base de datos, borra las tablas existentes (por seguridad)
    y las vuelve a crear desde cero según los modelos definidos.
    Luego, inserta los datos iniciales necesarios para que el sistema funcione.
    """
    print("Conectando a la base de datos para inicialización...")
    
    # Crear una instancia de la aplicación Flask temporalmente para tener el contexto
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        print("Borrando tablas existentes (si las hay)...")
        db.drop_all()
        
        print("Creando todas las tablas nuevas...")
        db.create_all()
        
        # --- INSERTAR DATOS INICIALES ESENCIALES ---
        session = SessionLocal()
        try:
            # Crear Roles
            print("Creando roles 'Administrador' y 'Vendedor'...")
            rol_admin = Rol(nombre='Administrador', descripcion='Acceso total al sistema')
            rol_vendedor = Rol(nombre='Vendedor', descripcion='Acceso al punto de venta y gestión de inventario')
            session.add(rol_admin)
            session.add(rol_vendedor)
            session.commit() # Guardamos los roles para obtener sus IDs

            # Crear Usuario Administrador por defecto
            print("Creando usuario 'admin' por defecto...")
            admin_password_hash = generate_password_hash('admin123') # Puedes cambiar esta contraseña si quieres
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
