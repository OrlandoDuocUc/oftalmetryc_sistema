#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORREGIR CONTRASEÑA EN POSTGRESQL
================================
"""

import psycopg2
from werkzeug.security import generate_password_hash

def corregir_password_admin():
    """Corregir la contraseña del usuario admin en PostgreSQL"""
    
    print("🔧 CORRIGIENDO CONTRASEÑA EN POSTGRESQL")
    print("=" * 45)
    
    try:
        # 1. Generar hash válido
        nueva_password = "admin"
        hash_valido = generate_password_hash(nueva_password)
        print(f"🔑 Hash generado para contraseña '{nueva_password}':")
        print(f"   {hash_valido}")
        
        # 2. Conectar a PostgreSQL
        print("\n🔌 Conectando a PostgreSQL...")
        conn = psycopg2.connect(
            host='localhost',
            database='optica_bd',
            user='postgres',
            password='12345',
            port=5432
        )
        cursor = conn.cursor()
        print("   ✅ Conexión exitosa")
        
        # 3. Verificar usuario actual
        print("\n🔍 Verificando usuario admin actual...")
        cursor.execute("SELECT usuario_id, username, password FROM usuarios WHERE username = 'admin';")
        result = cursor.fetchone()
        
        if result:
            user_id, username, old_password = result
            print(f"   👤 Usuario encontrado: {username} (ID: {user_id})")
            print(f"   🔑 Contraseña actual: '{old_password[:20]}...' (Longitud: {len(old_password)})")
        else:
            print("   ❌ Usuario admin no encontrado")
            return False
        
        # 4. Actualizar contraseña
        print("\n🔄 Actualizando contraseña...")
        cursor.execute(
            "UPDATE usuarios SET password = %s WHERE username = 'admin';",
            (hash_valido,)
        )
        
        # 5. Confirmar cambios
        conn.commit()
        rows_affected = cursor.rowcount
        print(f"   ✅ Contraseña actualizada ({rows_affected} fila(s) afectada(s))")
        
        # 6. Verificar actualización
        print("\n🔍 Verificando actualización...")
        cursor.execute("SELECT password FROM usuarios WHERE username = 'admin';")
        new_result = cursor.fetchone()
        
        if new_result:
            new_password_db = new_result[0]
            print(f"   ✅ Nueva contraseña en BD: {new_password_db[:30]}...")
            print(f"   📏 Longitud: {len(new_password_db)}")
            
            # Verificar que es un hash válido
            if new_password_db.startswith('scrypt:'):
                print("   ✅ Hash válido detectado")
            else:
                print("   ⚠️ Hash no parece ser formato scrypt")
        
        conn.close()
        
        print(f"\n🎉 ¡CORRECCIÓN COMPLETADA!")
        print(f"   Usuario: admin")
        print(f"   Contraseña: {nueva_password}")
        print(f"   Hash: {hash_valido[:30]}...")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = corregir_password_admin()
    if success:
        print("\n🚀 PRÓXIMO PASO: Ejecuta 'python boot.py' y prueba login con admin/admin")
    else:
        print("\n💥 Error en la corrección. Revisa los detalles arriba.")