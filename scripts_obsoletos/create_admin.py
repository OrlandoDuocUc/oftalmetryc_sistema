import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.domain.use_cases.services.user_service import UserService

# Crear usuario admin simple
user_service = UserService()

try:
    # Registrar usuario admin
    result = user_service.register_user(
        nombre='Admin',
        ap_pat='Sistema',
        ap_mat='',
        usuario='admin',
        email='admin@oftalmetryc.com',
        password='admin',
        rol='administrador'
    )
    print("✅ Usuario admin creado exitosamente")
    print(f"ID: {result}")
except Exception as e:
    print(f"❌ Error: {e}")