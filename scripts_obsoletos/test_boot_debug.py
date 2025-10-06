#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRUEBA SIMPLE DE LA APLICACIÓN
=============================
"""

print("🔍 PROBANDO ARRANQUE DE APLICACIÓN")
print("=" * 40)

try:
    # 1. Verificar imports básicos
    print("1️⃣ Probando imports básicos...")
    import os
    from dotenv import load_dotenv
    load_dotenv()
    print("   ✅ dotenv cargado")
    
    # 2. Verificar variables de entorno
    print("2️⃣ Verificando variables de entorno...")
    database_url = os.getenv('DATABASE_URL')
    print(f"   DATABASE_URL: {'✅ Configurada' if database_url else '❌ No encontrada'}")
    
    # 3. Intentar import de la app
    print("3️⃣ Intentando importar create_app...")
    from adapters.input.flask_app import create_app
    print("   ✅ create_app importado correctamente")
    
    # 4. Intentar crear la app
    print("4️⃣ Intentando crear la aplicación...")
    app = create_app()
    print("   ✅ App creada exitosamente")
    
    print("\n🎉 TODAS LAS PRUEBAS PASARON")
    print("La aplicación debería funcionar correctamente")
    
except Exception as e:
    print(f"\n❌ ERROR ENCONTRADO: {e}")
    print(f"Tipo de error: {type(e).__name__}")
    
    import traceback
    print("\n📋 TRACEBACK COMPLETO:")
    traceback.print_exc()