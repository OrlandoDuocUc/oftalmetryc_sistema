import os
from flask import Flask, redirect, url_for, request
from dotenv import load_dotenv
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

# ===================================================
#  CARGA DE ENTORNO
# ===================================================
load_dotenv()

print("===================================================")
print("🚀 INICIANDO SISTEMA OFTALMETRYC...")
print("===================================================")

# --- 1) CONFIGURACIÓN INICIAL ---
env = os.getenv("FLASK_ENV", "development")
database_url_raw = os.getenv("DATABASE_URL")

print(f"🌍 Entorno actual: {env.upper()}")
print(f"🔍 DATABASE_URL configurada: {'Sí' if database_url_raw else 'No'}")
if database_url_raw:
    print(f"🔗 DATABASE_URL original: {database_url_raw[:80]}...")

def _normalize_database_url(url: str) -> str:
    """
    - Cambia 'postgres://' a 'postgresql://'
    - En producción (host distinto a localhost/127.0.0.1) fuerza sslmode=require si no está dado.
    - Si no viene URL, retorna un fallback local (ajústalo si usas otro).
    """
    if not url:
        return "postgresql://postgres:postgres@localhost:5432/optica_db"

    p = urlparse(url)
    scheme = "postgresql" if p.scheme == "postgres" else p.scheme

    q = dict(parse_qsl(p.query or "", keep_blank_values=True))
    host_is_local = p.hostname in ("localhost", "127.0.0.1")
    if not host_is_local and "sslmode" not in q:
        q["sslmode"] = "require"

    new_query = urlencode(q)
    return urlunparse(p._replace(scheme=scheme, query=new_query))

database_url = _normalize_database_url(database_url_raw)
os.environ["DATABASE_URL"] = database_url  # para que la lea create_app
print(f"✅ DATABASE_URL normalizada: {database_url[:80]}...")

# --- 2) CREACIÓN DE LA APLICACIÓN ---
try:
    from adapters.input.flask_app import create_app
    app: Flask = create_app(config_name=env)
    print("✅ Aplicación principal y controladores cargados correctamente.")
    print(f"🗄️ SQLAlchemy URI en app.config: {str(app.config.get('SQLALCHEMY_DATABASE_URI', 'No configurado'))[:80]}...")
except Exception as e:
    print("\n" + "=" * 50)
    print("❌ ERROR CRÍTICO AL CARGAR LA APLICACIÓN PRINCIPAL")
    print(f"Error: {e}")
    print("=" * 50)
    print("🔍 Revisa las importaciones o si falta instalar alguna dependencia.")
    raise

# Si por alguna razón la factory no tomó la env var, asegúrate de que quede seteada:
if not app.config.get("SQLALCHEMY_DATABASE_URI") and database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    print("ℹ️ SQLALCHEMY_DATABASE_URI se fijó desde DATABASE_URL normalizada.")

# --- 2.1) REGISTRO DE BLUEPRINTS ADICIONALES (VENTAS - PÁGINAS) ---
try:
    if "sale_html" not in app.blueprints:
        from adapters.input.flask_app.sale_pages_routes import sale_html
        app.register_blueprint(sale_html)
        print("🧩 Blueprint 'sale_html' registrado correctamente.")
    else:
        print("ℹ️ Blueprint 'sale_html' ya estaba registrado; se omite.")
except Exception as e:
    print("\n" + "=" * 50)
    print("❌ ERROR al registrar el blueprint 'sale_html'")
    print(f"Error: {e}")
    print("=" * 50)
    raise

# --- 3) CONFIGURACIÓN DE RUTAS POR ENTORNO ---
def _is_local_mode(env_name: str, db_url: str) -> bool:
    if env_name == "development":
        return True
    try:
        host = urlparse(db_url or "").hostname
        return host in ("localhost", "127.0.0.1")
    except Exception:
        return False

is_local = _is_local_mode(env, database_url)

if is_local:
    print("🏠 MODO DESARROLLO LOCAL DETECTADO")
    @app.route("/")
    def index():
        return redirect(url_for("user_html.login"))
    print("✅ Ruta principal '/' configurada para redirigir al login (local).")
else:
    print("🌐 MODO PRODUCCIÓN DETECTADO")
    @app.route("/")
    def index_prod():
        return redirect(url_for("user_html.login"))

# --- 3.1) COMMIT/ROLLBACK AUTOMÁTICOS POR REQUEST ---
# Intentamos importar la instancia de SQLAlchemy 'db' desde rutas típicas.
db = None
_import_errors = []

for candidate in (
    "adapters.output.db",   # ej. adapters/output/db.py -> db = SQLAlchemy()
    "models",               # ej. models.py -> db = SQLAlchemy()
    "app.models",           # ej. app/models.py
    "adapters.input.flask_app.models",  # por si está ahí
):
    try:
        mod = __import__(candidate, fromlist=["db"])
        if hasattr(mod, "db"):
            db = getattr(mod, "db")
            print(f"🧬 Instancia 'db' importada desde: {candidate}")
            break
    except Exception as e:
        _import_errors.append(f"{candidate}: {e}")

if db is None:
    print("⚠️ No se pudo importar 'db' automáticamente. Commit/rollback automáticos deshabilitados.")
    for line in _import_errors[:3]:
        print(f"   • {line}")
else:
    @app.after_request
    def _commit_on_success(response):
        """
        Si el request muta datos y la respuesta es exitosa (<400), hacemos commit.
        (Incluye redirecciones 3xx post-INSERT).
        En cualquier otro caso, limpiamos con rollback.
        """
        try:
            if request.method in ("POST", "PUT", "PATCH", "DELETE") and response.status_code < 400:
                db.session.commit()
            else:
                db.session.rollback()
        except Exception:
            db.session.rollback()
            raise
        return response

    @app.teardown_request
    def _remove_session_on_teardown(exc=None):
        # Si hubo excepción, garantizamos rollback. Luego removemos la sesión.
        try:
            if exc is not None:
                db.session.rollback()
        finally:
            db.session.remove()

# --- 4) ARRANQUE DEL SERVIDOR (solo local / debug) ---
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    if is_local:
        host = "127.0.0.1"
        debug = True
    else:
        host = "0.0.0.0"
        debug = False

    print("---------------------------------------------------")
    print(f"🔧 Debug habilitado: {debug}")
    print(f"🌐 Iniciando servidor en http://{host}:{port}")
    print("---------------------------------------------------")
    app.run(host=host, port=port, debug=debug)
