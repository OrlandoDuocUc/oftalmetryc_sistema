#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar y corregir contraseñas en Render
"""

import os
import psycopg2
from werkzeug.security import generate_password_hash

def fix_passwords():
    """Corregir contraseñas en base de datos de Render"""
    try:
        # Obtener DATABASE_URL de Render
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("❌ DATABASE_URL no encontrada")
            return False
            
        print(f"🔗 Conectando a base de datos: {database_url[:50]}...")
        
        # Conectar a la base de datos
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("✅ Conexión exitosa")
        
        # Generar hash correcto para admin123
        correct_hash = generate_password_hash('admin123')
        print(f"🔐 Nuevo hash para admin123: {correct_hash[:50]}...")
        
        # Actualizar contraseña del usuario admin
        cursor.execute("""
            UPDATE usuario 
            SET password = %s 
            WHERE username = 'admin'
        """, (correct_hash,))
        
        rows_affected = cursor.rowcount
        print(f"📝 Filas actualizadas: {rows_affected}")
        
        # Verificar la actualización
        cursor.execute("SELECT username, password FROM usuario WHERE username = 'admin'")
        result = cursor.fetchone()
        
        if result:
            username, stored_hash = result
            print(f"✅ Usuario: {username}")
            print(f"🔐 Hash almacenado: {stored_hash[:50]}...")
        
        conn.commit()
        conn.close()
        
        print("✅ Contraseña actualizada correctamente")
        print("🔐 Nuevas credenciales: admin / admin123")
        return True
            
    except Exception as e:
        print(f"❌ Error corrigiendo contraseñas: {e}")
        return False

if __name__ == "__main__":
    fix_passwords()