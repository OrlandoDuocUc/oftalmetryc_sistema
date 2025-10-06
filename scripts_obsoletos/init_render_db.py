#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para inicializar la base de datos en Render
Verifica e inserta datos básicos si no existen
"""

import os
import psycopg2
from psycopg2 import sql

def init_render_database():
    """Inicializar base de datos en Render con datos básicos"""
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
        
        # Verificar si ya existen usuarios
        cursor.execute("SELECT COUNT(*) FROM usuario WHERE username = 'admin'")
        admin_count = cursor.fetchone()[0]
        
        if admin_count > 0:
            print("✅ Usuario admin ya existe")
            conn.close()
            return True
            
        print("🔧 Insertando datos básicos...")
        
        # Insertar rol de administrador si no existe
        cursor.execute("""
            INSERT INTO rol (nombre, descripcion, estado) 
            VALUES ('Administrador', 'Administrador del sistema', 'A')
            ON CONFLICT DO NOTHING
            RETURNING rol_id
        """)
        
        result = cursor.fetchone()
        if result:
            rol_id = result[0]
        else:
            # Si ya existe, obtener el ID
            cursor.execute("SELECT rol_id FROM rol WHERE nombre = 'Administrador' LIMIT 1")
            rol_id = cursor.fetchone()[0]
        
        # Insertar usuario admin
        cursor.execute("""
            INSERT INTO usuario (nombre, ap_pat, ap_mat, username, email, password, estado, rol_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (username) DO NOTHING
        """, (
            'Administrador',
            'Sistema', 
            '', 
            'admin', 
            'admin@oftalmetryc.com', 
            'scrypt:32768:8:1$YNx7QtiZ2BTdqWeB$56f458904cb782fd026c1b4f11fe75c59c9b2e92b48fd0e09f084d29add66d3362a3b2adfdbce70e41f2df68377128072031785b0ff1201ac51040cf1da9b4f4', 
            'A', 
            rol_id
        ))
        
        # Verificar inserción
        cursor.execute("SELECT COUNT(*) FROM usuario WHERE username = 'admin'")
        final_count = cursor.fetchone()[0]
        
        conn.commit()
        conn.close()
        
        if final_count > 0:
            print("✅ Usuario admin creado exitosamente")
            print("🔐 Credenciales: admin / admin123")
            return True
        else:
            print("❌ Error al crear usuario admin")
            return False
            
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        return False

if __name__ == "__main__":
    init_render_database()