#!/usr/bin/env python3
"""
CORREGIR CONEXIÓN A RENDER - Ficha Clínica
Script para corregir la configuración y que GitHub se conecte correctamente a Render
"""
import os
import shutil

def corregir_conexion_render():
    """Corrige la configuración para conectar correctamente a Render"""
    print("🔧 CORRIGIENDO CONEXIÓN A RENDER PARA GITHUB...")
    
    # 1. Restaurar controlador original
    print("\n1️⃣ Restaurando controlador original...")
    try:
        if os.path.exists("adapters/input/flask_app/controllers/consulta_medica_controller_backup.py"):
            shutil.copy2(
                "adapters/input/flask_app/controllers/consulta_medica_controller_backup.py",
                "adapters/input/flask_app/controllers/consulta_medica_controller.py"
            )
            print("✅ Controlador restaurado")
        else:
            print("⚠️ Backup no encontrado, continuando...")
    except Exception as e:
        print(f"❌ Error restaurando controlador: {e}")
    
    # 2. Crear archivo .env para desarrollo local (conecta a Render)
    print("\n2️⃣ Configurando .env para desarrollo...")
    env_content = """# Configuración para desarrollo local conectando a Render
DATABASE_URL=postgresql://oftalmetryc_user:0WdPbRIzVrbH6xYFCye20Q7ST4e3v7Kn@dpg-d3efatffte5s73chd9r0-a.oregon-postgres.render.com/oftalmetryc_db
DB_USER=oftalmetryc_user
DB_PASSWORD=0WdPbRIzVrbH6xYFCye20Q7ST4e3v7Kn
DB_HOST=dpg-d3efatffte5s73chd9r0-a.oregon-postgres.render.com
DB_PORT=5432
DB_NAME=oftalmetryc_db

# Configuración de Encoding UTF-8
PGCLIENTENCODING=UTF8
PYTHONIOENCODING=utf-8

# Configuración de Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=optica-almonacid-secret-key-2024

# Configuración de zona horaria
TIMEZONE=America/Santiago
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Archivo .env configurado para Render")
    except Exception as e:
        print(f"❌ Error configurando .env: {e}")
    
    # 3. Verificar que settings.py esté correcto
    print("\n3️⃣ Verificando settings.py...")
    try:
        with open('config/settings.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'oftalmetryc_db' in content:
                print("✅ settings.py configurado correctamente")
            else:
                print("⚠️ Revisar settings.py manualmente")
    except Exception as e:
        print(f"❌ Error verificando settings.py: {e}")
    
    # 4. Crear script de verificación
    print("\n4️⃣ Creando script de verificación...")
    verificacion_content = '''#!/usr/bin/env python3
"""
Script para verificar que la conexión a Render funciona
"""
import os
from app.infraestructure.utils.db import get_connection

def verificar_conexion():
    """Verifica la conexión a la base de datos de Render"""
    try:
        print("🔄 Verificando conexión a Render...")
        conn = get_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM paciente;")
            pacientes = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM consulta_medica;")
            consultas = cur.fetchone()[0]
            
            print(f"✅ Conexión exitosa a Render:")
            print(f"   📋 Pacientes: {pacientes}")
            print(f"   👁️ Consultas médicas: {consultas}")
            
            cur.close()
            conn.close()
            return True
        else:
            print("❌ No se pudo conectar a la base de datos")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    verificar_conexion()
'''
    
    try:
        with open('verificar_conexion_render.py', 'w', encoding='utf-8') as f:
            f.write(verificacion_content)
        print("✅ Script de verificación creado")
    except Exception as e:
        print(f"❌ Error creando script de verificación: {e}")
    
    print("\n🎉 ¡CORRECCIÓN COMPLETADA!")
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. 🧪 Ejecutar: python verificar_conexion_render.py")
    print("2. 🚀 Ejecutar: python boot.py")
    print("3. 🌐 Subir cambios a GitHub")
    print("4. ✅ Deploy automático en Render")
    print("\n🔗 URL Render: https://oftalmetryc-sistema.onrender.com")

if __name__ == "__main__":
    corregir_conexion_render()