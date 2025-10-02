#!/usr/bin/env python3
"""
Script para verificar las tablas existentes en la base de datos
"""
from app.infraestructure.utils.db import engine
from sqlalchemy import text

def check_tables():
    try:
        print("🔍 Verificando tablas existentes en la base de datos...")
        
        with engine.connect() as connection:
            # Obtener todas las tablas
            result = connection.execute(text("""
                SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, IS_NULLABLE
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = 'dbo'
                ORDER BY TABLE_NAME, ORDINAL_POSITION
            """))
            
            tables = {}
            for row in result:
                table_name = row[0]
                if table_name not in tables:
                    tables[table_name] = []
                tables[table_name].append({
                    'column': row[1],
                    'type': row[2],
                    'nullable': row[3]
                })
            
            if tables:
                print("📋 Tablas encontradas:")
                for table_name, columns in tables.items():
                    print(f"\n   🗂️ Tabla: {table_name}")
                    for col in columns:
                        nullable = "NULL" if col['nullable'] == 'YES' else "NOT NULL"
                        print(f"      - {col['column']}: {col['type']} ({nullable})")
            else:
                print("📭 No se encontraron tablas en la base de datos")
                
        return tables
        
    except Exception as e:
        print(f"❌ Error al verificar tablas: {str(e)}")
        return {}

if __name__ == "__main__":
    check_tables() 