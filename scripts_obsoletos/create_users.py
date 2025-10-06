import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine, text

# Cargar variables de entorno
load_dotenv()

# Usar SQLAlchemy para evitar problemas de encoding
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://oouser:OO123456@localhost:5432/oftalmetryc')
engine = create_engine(DATABASE_URL)

# Usar SQLAlchemy para evitar problemas de encoding
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://oouser:OO123456@localhost:5432/oftalmetryc')
engine = create_engine(DATABASE_URL)

# Generar hashes
admin_hash = generate_password_hash('admin')
orlando_hash = generate_password_hash('orlando')

print(f"Hash admin: {admin_hash}")
print(f"Hash orlando: {orlando_hash}")

# Insertar usuarios usando SQLAlchemy
try:
    with engine.connect() as conn:
        # Usuario admin
        conn.execute(text("""
            INSERT INTO usuario (nombre, ap_pat, ap_mat, username, email, password, estado, rol_id) 
            VALUES (:nombre, :ap_pat, :ap_mat, :username, :email, :password, :estado, :rol_id)
        """), {
            'nombre': 'Administrador',
            'ap_pat': 'Sistema', 
            'ap_mat': '',
            'username': 'admin',
            'email': 'admin@oftalmetryc.com',
            'password': admin_hash,
            'estado': 'A',
            'rol_id': 1
        })
        
        # Usuario orlando
        conn.execute(text("""
            INSERT INTO usuario (nombre, ap_pat, ap_mat, username, email, password, estado, rol_id) 
            VALUES (:nombre, :ap_pat, :ap_mat, :username, :email, :password, :estado, :rol_id)
        """), {
            'nombre': 'Orlando',
            'ap_pat': 'Usuario',
            'ap_mat': 'Vendedor',
            'username': 'orlando',
            'email': 'orlando@oftalmetryc.com',
            'password': orlando_hash,
            'estado': 'A',
            'rol_id': 2
        })
        
        conn.commit()
        print("✅ Usuarios creados exitosamente")
        
        # Verificar usuarios creados
        result = conn.execute(text("SELECT usuario_id, nombre, username, rol_id FROM usuario"))
        users = result.fetchall()
        print("\n📋 Usuarios en la base de datos:")
        for user in users:
            print(f"ID: {user[0]}, Nombre: {user[1]}, Username: {user[2]}, Rol ID: {user[3]}")
        
except Exception as e:
    print(f"❌ Error: {e}")