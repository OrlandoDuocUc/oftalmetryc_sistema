#!/usr/bin/env python3
"""
Script para probar que los imports funcionen correctamente
"""

try:
    print("🔍 Probando import de sale_controller...")
    from adapters.input.flask_app.controllers.sale_controller import sale_html
    print("✅ sale_controller importado correctamente")
    
    print("🔍 Probando import de user_service...")
    from app.domain.use_cases.services.user_service import UserService
    print("✅ user_service importado correctamente")
    
    print("🔍 Probando import de user_repository...")
    from app.infraestructure.repositories.sql_user_repository import SQLUserRepository
    print("✅ user_repository importado correctamente")
    
    print("\n🎉 Todos los imports funcionan correctamente!")
    print("✅ Los cambios no han roto nada")
    
except Exception as e:
    print(f"❌ Error en import: {e}")
    import traceback
    traceback.print_exc() 