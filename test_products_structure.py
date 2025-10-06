#!/usr/bin/env python3
"""
Script para verificar la estructura de productos y los campos faltantes en el frontend
"""
import os
import sys

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.infraestructure.utils.db import get_connection

def test_products_structure():
    """
    Verificar estructura de productos y campos faltantes
    """
    print("=== VERIFICACIÓN ESTRUCTURA DE PRODUCTOS ===")
    
    conn = None
    try:
        # Conectar a la base de datos
        conn = get_connection()
        cursor = conn.cursor()
        
        # 1. Verificar estructura de tabla productos
        print("\n1. Verificando tabla productos...")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'productos'
            ORDER BY ordinal_position
        """)
        
        product_columns = cursor.fetchall()
        print(f"Columnas en productos: {len(product_columns)}")
        for col, dtype, nullable, default in product_columns:
            print(f"  - {col}: {dtype} {'(NULL)' if nullable == 'YES' else '(NOT NULL)'} {f'DEFAULT {default}' if default else ''}")
        
        # 2. Verificar datos existentes
        print("\n2. Verificando productos existentes...")
        cursor.execute("SELECT COUNT(*) FROM productos WHERE estado = true")
        count = cursor.fetchone()[0]
        print(f"Total productos activos: {count}")
        
        if count > 0:
            cursor.execute("""
                SELECT producto_id, nombre, categoria, marca, sku, stock, precio_unitario
                FROM productos 
                WHERE estado = true
                ORDER BY fecha_creacion DESC
                LIMIT 3
            """)
            
            recent_products = cursor.fetchall()
            print("\nÚltimos productos:")
            for prod in recent_products:
                print(f"  - ID: {prod[0]}, Nombre: {prod[1]}")
                print(f"    Categoría: {prod[2] or 'N/A'}, Marca: {prod[3] or 'N/A'}, SKU: {prod[4] or 'N/A'}")
                print(f"    Stock: {prod[5]}, Precio: ${prod[6]}")
        
        print("\n=== RESUMEN ===")
        print("✅ Conexión a base de datos: OK")
        print(f"✅ Productos activos: {count}")
        
        return True, product_columns
        
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
        return False, []
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    success, columns = test_products_structure()
    if success:
        print("\n🎉 Verificación completada exitosamente")
        print("\nCampos disponibles en BD pero que pueden faltar en frontend:")
        frontend_fields = ["nombre", "descripcion", "precio_unitario", "stock"]
        db_fields = [col[0] for col in columns]
        
        missing_in_frontend = [field for field in db_fields if field not in frontend_fields and field not in ['producto_id', 'estado', 'fecha_creacion']]
        
        for field in missing_in_frontend:
            print(f"  - {field}")
    else:
        print("\n💥 Error en la verificación")