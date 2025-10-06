#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFICAR CONTRASEÑA DEL USUARIO ADMIN
=====================================
"""

import psycopg2

def verificar_password_admin():
    """Verificar la contraseña exacta del usuario admin"""
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='optica_bd',
            user='postgres',
            password='12345',
            port=5432
        )
        cursor = conn.cursor()
        
        cursor.execute("SELECT usuario_id, username, password FROM usuarios WHERE username = 'admin';")
        
        result = cursor.fetchone()
        if result:
            user_id, username, password = result
            print(f"👤 Usuario: {username}")
            print(f"🔑 Contraseña: '{password}'")
            print(f"📏 Longitud: {len(password)}")
            print(f"💡 Tipo: {type(password)}")
            print(f"🔍 Contiene '$': {'$' in password}")
            print(f"📋 Repr: {repr(password)}")
        else:
            print("❌ Usuario admin no encontrado")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    verificar_password_admin()