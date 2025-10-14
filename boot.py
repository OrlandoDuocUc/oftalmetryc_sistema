import os
from flask import Flask, redirect, url_for
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

print("===================================================")
print("🚀 INICIANDO SISTEMA OFTALMETRYC...")
print("===================================================")

# --- 1. CONFIGURACIÓN INICIAL ---
env = os.getenv('FLASK_ENV', 'development')
database_url = os.getenv('DATABASE_URL')

print(f"🌍 Entorno actual: {env.upper()}")
print(f"🔍 DATABASE_URL configurada: {'Sí' if database_url else 'No'}")
if database_url:
    print(f"🔗 Usando DATABASE_URL: {database_url[:50]}...")

# --- 2. CREACIÓN DE LA APLICACIÓN ---
try:
    from adapters.input.flask_app import create_app
    app = create_app(config_name=env)
    print("✅ Aplicación principal y controladores cargados correctamente.")
    print(f"🗄️ SQLAlchemy URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'No configurado')[:50]}...")
except Exception as e:
    print("\n" + "="*50)
    print("❌ ERROR CRÍTICO AL CARGAR LA APLICACIÓN PRINCIPAL")
    print(f"Error: {e}")
    print("="*50)
    print("🔍 Revisa las importaciones o si falta instalar alguna dependencia.")
    raise

# --- 2.1 REGISTRO DE BLUEPRINTS ADICIONALES (VENTAS - PÁGINAS) ---
try:
    # Registrar sólo si no está ya registrado
    if 'sale_html' not in app.blueprints:
        from adapters.input.flask_app.sale_pages_routes import sale_html
        app.register_blueprint(sale_html)
        print("🧩 Blueprint 'sale_html' registrado correctamente.")
    else:
        print("ℹ️ Blueprint 'sale_html' ya estaba registrado; se omite.")
except Exception as e:
    print("\n" + "="*50)
    print("❌ ERROR al registrar el blueprint 'sale_html'")
    print(f"Error: {e}")
    print("="*50)
    raise

# --- 3. CONFIGURACIÓN DE RUTAS POR ENTORNO ---
is_local = (env == 'development') or ('localhost' in database_url if database_url else False)

if is_local:
    # --- LÓGICA PARA ENTORNO LOCAL ---
    print("🏠 MODO DESARROLLO LOCAL DETECTADO")
    try:
        # La factory 'create_app' ya registró los otros blueprints.
        @app.route('/')
        def index():
            # Redirigir automáticamente a la página de login
            return redirect(url_for('user_html.login'))
        print("✅ Ruta principal '/' configurada para redirigir al login (local).")
    except Exception as e:
        print("\n" + "="*50)
        print("❌ ERROR AL CONFIGURAR LA RUTA LOCAL '/'")
        print(f"Error: {e}")
        print("="*50)
        raise
else:
    # --- LÓGICA PARA ENTORNO DE PRODUCCIÓN ---
    print("🌐 MODO PRODUCCIÓN DETECTADO")
    @app.route('/')
    def index_prod():
        return redirect(url_for('user_html.login'))

# --- 4. ARRANQUE DEL SERVIDOR ---
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    if is_local:
        host = '127.0.0.1'
        debug = True
    else:
        host = '0.0.0.0'
        debug = False

    print("---------------------------------------------------")
    print(f"🔧 Debug habilitado: {debug}")
    print(f"🌐 Iniciando servidor en http://{host}:{port}")
    print("---------------------------------------------------")
    app.run(host=host, port=port, debug=debug)
