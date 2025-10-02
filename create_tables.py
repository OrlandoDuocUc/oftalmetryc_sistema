#!/usr/bin/env python3
"""
Script para crear las tablas en la base de datos
"""
from app.infraestructure.utils.init_db import Base, engine
from app.infraestructure.utils.models import User, Product, Sale

def create_tables():
    try:
        print("🔨 Creando tablas en la base de datos...")
        
        # Crear todas las tablas
        Base.metadata.create_all(bind=engine, checkfirst=True)
        
        print("✅ Tablas creadas exitosamente!")
        print("📋 Tablas creadas:")
        print("   - usuario (Users)")
        print("   - producto (Products)") 
        print("   - venta (Sales)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al crear las tablas: {str(e)}")
        return False

if __name__ == "__main__":
    create_tables() 