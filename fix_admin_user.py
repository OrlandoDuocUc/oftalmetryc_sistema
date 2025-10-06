#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para verificar y corregir el usuario admin
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.infraestructure.utils.db import SessionLocal
from app.domain.models.user import User
from werkzeug.security import generate_password_hash
import traceback

def check_admin_user():
    """Verifica el usuario admin y su password"""
    print("🔍 VERIFICANDO USUARIO ADMIN")
    print("=" * 40)
    
    try:
        session = SessionLocal()
        try:
            # Buscar usuario admin
            admin_user = session.query(Usuario).filter_by(username='admin').first()
            
            if admin_user:
                print(f"✅ Usuario admin encontrado:")
                print(f"   - ID: {admin_user.usuario_id}")
                print(f"   - Username: {admin_user.username}")
                print(f"   - Nombre: {admin_user.nombre}")
                print(f"   - Email: {admin_user.email}")
                print(f"   - Estado: {admin_user.estado}")
                print(f"   - Password length: {len(admin_user.password) if admin_user.password else 0}")
                print(f"   - Password value: '{admin_user.password}'")
                
                # Verificar si el password está hasheado correctamente
                if not admin_user.password or len(admin_user.password) < 10:
                    print("❌ Password está vacío o es muy corto")
                    return False, admin_user
                elif not admin_user.password.startswith('$'):
                    print("❌ Password no está hasheado (no empieza con $)")
                    return False, admin_user
                else:
                    print("✅ Password parece estar hasheado correctamente")
                    return True, admin_user
            else:
                print("❌ Usuario admin NO encontrado")
                return False, None
                
        finally:
            session.close()
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        traceback.print_exc()
        return False, None

def fix_admin_password():
    """Corrige el password del usuario admin"""
    print("\n🔧 CORRIGIENDO PASSWORD DEL ADMIN")
    print("=" * 40)
    
    try:
        session = SessionLocal()
        try:
            # Buscar usuario admin
            admin_user = session.query(Usuario).filter_by(username='admin').first()
            
            if admin_user:
                # Generar nuevo password hasheado para 'admin123'
                new_password_hash = generate_password_hash('admin123')
                print(f"🔐 Nuevo hash generado: {new_password_hash[:50]}...")
                
                # Actualizar password
                admin_user.password = new_password_hash
                session.commit()
                
                print("✅ Password del admin actualizado exitosamente")
                print("🔑 Credenciales:")
                print("   Username: admin")
                print("   Password: admin123")
                
                return True
            else:
                print("❌ Usuario admin no encontrado para actualizar")
                return False
                
        finally:
            session.close()
            
    except Exception as e:
        print(f"❌ Error actualizando password: {str(e)}")
        traceback.print_exc()
        return False

def create_admin_user():
    """Crea un nuevo usuario admin si no existe"""
    print("\n🆕 CREANDO USUARIO ADMIN")
    print("=" * 40)
    
    try:
        session = SessionLocal()
        try:
            # Verificar si ya existe
            existing_admin = session.query(Usuario).filter_by(username='admin').first()
            if existing_admin:
                print("⚠️ Usuario admin ya existe, no se puede crear otro")
                return False
            
            # Crear nuevo usuario admin
            password_hash = generate_password_hash('admin123')
            
            nuevo_admin = Usuario(
                rol_id=1,  # Asumiendo que el rol 1 es Administrador
                username='admin',
                password=password_hash,
                nombre='Administrador',
                ap_pat='Sistema',
                ap_mat='',
                email='admin@opticamaipu.cl',
                estado=True
            )
            
            session.add(nuevo_admin)
            session.commit()
            session.refresh(nuevo_admin)
            
            print(f"✅ Usuario admin creado con ID: {nuevo_admin.usuario_id}")
            print("🔑 Credenciales:")
            print("   Username: admin")
            print("   Password: admin123")
            
            return True
            
        finally:
            session.close()
            
    except Exception as e:
        print(f"❌ Error creando admin: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 DIAGNÓSTICO Y CORRECCIÓN DEL USUARIO ADMIN")
    print("=" * 50)
    
    # 1. Verificar usuario admin actual
    is_valid, admin_user = check_admin_user()
    
    if admin_user and not is_valid:
        # 2. Si existe pero tiene problemas, corregir password
        success = fix_admin_password()
        if success:
            print("\n🎉 Password corregido. Prueba iniciar sesión con:")
            print("   Username: admin")
            print("   Password: admin123")
    elif not admin_user:
        # 3. Si no existe, crear usuario admin
        success = create_admin_user()
        if success:
            print("\n🎉 Usuario admin creado. Prueba iniciar sesión con:")
            print("   Username: admin")
            print("   Password: admin123")
    else:
        print("\n✅ Usuario admin está bien configurado")
        print("🔑 Intenta iniciar sesión con:")
        print("   Username: admin")
        print("   Password: admin123")