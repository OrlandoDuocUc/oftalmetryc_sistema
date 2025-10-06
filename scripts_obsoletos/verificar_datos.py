import os
import sys
from dotenv import load_dotenv
import psycopg2

# Cargar variables de entorno
load_dotenv()

def verificar_datos():
    try:
        # Usar credenciales individuales
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        database = os.getenv('DB_NAME')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        
        # Conectar usando parámetros individuales
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            client_encoding='utf8'
        )
        
        cursor = conn.cursor()
        
        print("=== VERIFICACIÓN DE DATOS ===")
        
        # Verificar roles
        cursor.execute("SELECT COUNT(*) FROM roles;")
        roles_count = cursor.fetchone()[0]
        print(f"Roles: {roles_count} registros")
        
        if roles_count > 0:
            cursor.execute("SELECT rol_id, nombre FROM roles;")
            roles = cursor.fetchall()
            print("Roles encontrados:")
            for rol in roles:
                print(f"  - ID: {rol[0]}, Nombre: {rol[1]}")
        
        print("-" * 40)
        
        # Verificar usuarios
        cursor.execute("SELECT COUNT(*) FROM usuarios;")
        usuarios_count = cursor.fetchone()[0]
        print(f"Usuarios: {usuarios_count} registros")
        
        if usuarios_count > 0:
            cursor.execute("SELECT usuario_id, username, nombre FROM usuarios;")
            usuarios = cursor.fetchall()
            print("Usuarios encontrados:")
            for usuario in usuarios:
                print(f"  - ID: {usuario[0]}, Username: {usuario[1]}, Nombre: {usuario[2]}")
        else:
            print("⚠️ NO HAY USUARIOS - Esto explica el error de login")
            print("💡 SOLUCION: Insertar usuario admin")
        
        print("-" * 40)
        
        # Verificar productos
        cursor.execute("SELECT COUNT(*) FROM productos;")
        productos_count = cursor.fetchone()[0]
        print(f"Productos: {productos_count} registros")
        
        print("-" * 40)
        
        # Verificar tablas médicas
        tablas_medicas = ['pacientes_medicos', 'fichas_clinicas', 'biomicroscopia']
        for tabla in tablas_medicas:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla};")
            count = cursor.fetchone()[0]
            print(f"{tabla}: {count} registros")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    verificar_datos()