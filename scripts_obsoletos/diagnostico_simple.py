#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIAGNÓSTICO SIMPLE DE IMPORTACIÓN
================================
"""

print("🔍 PROBANDO IMPORTACIONES PASO A PASO")
print("=" * 40)

try:
    print("1️⃣ Importando dotenv...")
    from dotenv import load_dotenv
    load_dotenv()
    print("   ✅ dotenv OK")
    
    print("2️⃣ Verificando DATABASE_URL...")
    import os
    database_url = os.getenv('DATABASE_URL')
    print(f"   DATABASE_URL: {'✅ Encontrada' if database_url else '❌ No encontrada'}")
    
    print("3️⃣ Intentando importar create_app...")
    from adapters.input.flask_app import create_app
    print("   ✅ create_app importado")
    
    print("4️⃣ Intentando crear app...")
    app = create_app()
    print("   ✅ App creada exitosamente")
    
    print("5️⃣ Probando app básica...")
    print(f"   App name: {app.name}")
    print(f"   Config: {type(app.config)}")
    
    print("\n🎉 ¡TODO FUNCIONÓ! El problema debe estar en boot.py")
    
except Exception as e:
    print(f"\n❌ ERROR EN PASO: {e}")
    print(f"Tipo: {type(e).__name__}")
    
    import traceback
    print("\n📋 TRACEBACK COMPLETO:")
    traceback.print_exc()