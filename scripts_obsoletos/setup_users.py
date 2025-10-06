# Script para crear usuarios desde Flask app
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from werkzeug.security import generate_password_hash
from app.infraestructure.utils.db import SessionLocal
from app.domain.models.user import User

# Crear sesión de base de datos
session = SessionLocal()

try:
    # Limpiar usuarios existentes
    session.query(User).delete()
    
    # Crear usuario admin
    admin_hash = generate_password_hash('admin')
    admin_user = User(
        nombre='Administrador',
        ap_pat='Sistema',
        ap_mat='',
        username='admin',
        email='admin@oftalmetryc.com',
        password=admin_hash,
        estado='A',
        rol_id=1
    )
    
    # Crear usuario orlando
    orlando_hash = generate_password_hash('orlando')
    orlando_user = User(
        nombre='Orlando',
        ap_pat='Usuario',
        ap_mat='Vendedor',
        username='orlando',
        email='orlando@oftalmetryc.com',
        password=orlando_hash,
        estado='A',
        rol_id=2
    )
    
    # Agregar a la sesión
    session.add(admin_user)
    session.add(orlando_user)
    
    # Confirmar cambios
    session.commit()
    
    print("✅ Usuarios creados exitosamente:")
    print(f"  - admin (hash: {admin_hash[:50]}...)")
    print(f"  - orlando (hash: {orlando_hash[:50]}...)")
    
    # Verificar usuarios
    usuarios = session.query(User).all()
    print(f"\n📋 Total usuarios en BD: {len(usuarios)}")
    for user in usuarios:
        print(f"  - {user.username} ({user.nombre})")
        
except Exception as e:
    print(f"❌ Error: {e}")
    session.rollback()
finally:
    session.close()