#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.infraestructure.utils.db import SessionLocal
from app.domain.models.user import User
from werkzeug.security import generate_password_hash

def fix_admin():
    session = SessionLocal()
    try:
        # Buscar admin
        admin = session.query(User).filter_by(username='admin').first()
        
        if admin:
            print(f"👤 Admin encontrado: {admin.username}")
            print(f"🔐 Password actual: '{admin.password}'")
            print(f"📏 Longitud password: {len(admin.password) if admin.password else 0}")
            
            # Crear nuevo password hasheado
            new_hash = generate_password_hash('admin123')
            admin.password = new_hash
            session.commit()
            
            print("✅ Password actualizado!")
            print("🔑 Credenciales: admin / admin123")
        else:
            print("❌ Usuario admin no encontrado")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    fix_admin()