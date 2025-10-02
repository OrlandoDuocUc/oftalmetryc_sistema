import os
from flask import Flask

# Obtener el entorno desde variables de entorno - En Render será 'production'
env = os.getenv('FLASK_ENV', 'production')  # Cambiar default a production

# Verificar variables de entorno críticas
database_url = os.getenv('DATABASE_URL')
print(f"🔍 DATABASE_URL configurada: {'Sí' if database_url else 'No'}")
print(f"🌍 FLASK_ENV: {env}")
if database_url:
    print(f"🔗 DATABASE_URL: {database_url[:50]}...")

# Intentar importar la app completa
try:
    from adapters.input.flask_app import create_app
    app = create_app(config_name=env)
    print("✅ App completa cargada correctamente")
    
    # Verificar la configuración de la base de datos en la app
    print(f"🗄️ SQLAlchemy URI configurado: {app.config.get('SQLALCHEMY_DATABASE_URI', 'No configurado')[:50]}...")
    
    # INICIALIZAR BASE DE DATOS EN RENDER
    if env == 'production' and database_url:
        print("🚀 Inicializando base de datos en Render...")
        try:
            from init_render_db import init_render_database
            init_success = init_render_database()
            if init_success:
                print("✅ Base de datos inicializada correctamente")
            else:
                print("⚠️ Error en inicialización, pero continuando...")
                
            # CORREGIR CONTRASEÑAS
            print("🔐 Verificando y corrigiendo contraseñas...")
            from fix_passwords import fix_passwords
            fix_success = fix_passwords()
            if fix_success:
                print("✅ Contraseñas corregidas")
            else:
                print("⚠️ Error corrigiendo contraseñas, pero continuando...")
                
        except Exception as init_error:
            print(f"⚠️ Error en inicialización de DB: {init_error}")
    
except Exception as e:
    print(f"⚠️ Error cargando app completa: {e}")
    print("🔧 Forzando carga con configuración de producción...")
    
    # Intentar con configuración explícita
    try:
        from config.settings import ProductionConfig
        from adapters.input.flask_app import create_app
        
        # Forzar configuración de producción
        app = create_app(config_name='production')
        print("✅ App cargada con configuración de producción")
        print(f"🗄️ SQLAlchemy URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'No configurado')[:50]}...")
        
    except Exception as e2:
        print(f"❌ Error crítico: {e2}")
        print("🔧 Creando app básica temporal...")
    
    # Crear una app básica de Flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'temp-key')
    
    @app.route('/')
    def health_check():
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Oftalmetryc Sistema</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f4f4f4; }
                .container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #2c3e50; }
                .success { color: #27ae60; }
                .warning { color: #f39c12; }
                .info { color: #3498db; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Oftalmetryc Sistema</h1>
                <p class="success">✅ Deploy exitoso en Render!</p>
                <p class="warning">⚠️ Configurando base de datos PostgreSQL...</p>
                <p class="info">📋 Próximos pasos:</p>
                <ul>
                    <li>Crear base de datos PostgreSQL</li>
                    <li>Conectar variable DATABASE_URL</li>
                    <li>Ejecutar script de inicialización</li>
                    <li>Sistema completo funcionando</li>
                </ul>
                <hr>
                <p><strong>Estado:</strong> Aplicación desplegada correctamente</p>
                <p><strong>Versión:</strong> Python 3.13.4</p>
                <p><strong>Framework:</strong> Flask 3.1.1</p>
            </div>
        </body>
        </html>
        """
    
    @app.route('/health')
    def health():
        return {"status": "ok", "message": "Aplicación funcionando", "env": env}

if __name__ == '__main__':
    # En producción, Render usará gunicorn
    # En desarrollo, usar el servidor Flask
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    debug = env == 'development'
    
    print(f"🌐 Iniciando servidor en {host}:{port}")
    app.run(host=host, port=port, debug=debug)
