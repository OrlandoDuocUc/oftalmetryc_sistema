#!/usr/bin/env python3
"""
Script de inicialización para la base de datos en producción
"""
import os
import sys
from pathlib import Path

# Agregar el directorio raíz al PYTHONPATH
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

from app.infraestructure.utils.db import Database
from boot import app

def init_database():
    """Inicializa la base de datos con las tablas necesarias"""
    try:
        # Crear la conexión a la base de datos
        db = Database()
        
        # Leer el archivo SQL de tablas médicas
        sql_file = root_dir / 'medical_tables.sql'
        
        if sql_file.exists():
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # Ejecutar el SQL
            with db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql_content)
                conn.commit()
            
            print("✅ Base de datos inicializada correctamente")
            return True
        else:
            print("❌ Archivo medical_tables.sql no encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Inicializando base de datos...")
    
    # Verificar que las variables de entorno estén configuradas
    if not os.getenv('DATABASE_URL'):
        print("❌ DATABASE_URL no está configurada")
        sys.exit(1)
    
    success = init_database()
    sys.exit(0 if success else 1)