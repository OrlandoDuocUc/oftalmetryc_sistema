# adapters/input/flask_app/__init__.py

import os
from flask import Flask
from config.settings import config_by_name
from app.infraestructure.utils.currency_utils import format_currency_simple

# Blueprints existentes
from adapters.input.flask_app.controllers.user_controller import user_html
from adapters.input.flask_app.controllers.product_controller import product_html

# Usa SOLO el blueprint de páginas de venta nuevo (sale_pages_routes).
from adapters.input.flask_app.controllers.sale_pages_routes import sale_html

# Otros blueprints de tu app
from .routes import bp  # Blueprint principal con todas las rutas
from .medical_routes import medical_bp  # Rutas médicas
from .proveedor_routes import proveedor_bp  # Rutas de proveedores


def create_app(config_name: str = "development") -> Flask:
    # Config
    config_class = config_by_name.get(config_name, config_by_name["development"])

    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_folder = os.path.join(base_dir, "templates")
    static_folder = os.path.join(base_dir, "static")

    # ⚠️ Renombramos a 'flask_app' para no chocar con el paquete 'app'
    flask_app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    flask_app.config.from_object(config_class)

    # SECRET_KEY es NECESARIA porque usamos 'session' para el flujo de venta
    if not flask_app.config.get("SECRET_KEY"):
        flask_app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

    # Para recargar plantillas en dev (opcional)
    flask_app.config.setdefault("TEMPLATES_AUTO_RELOAD", True)

    # Filtro de moneda usado en tus templates: {{ valor|currency }}
    flask_app.jinja_env.filters["currency"] = format_currency_simple

    # ────────────── Registro de Blueprints (evita doble registro) ──────────────
    if "user_html" not in flask_app.blueprints:
        flask_app.register_blueprint(user_html)

    if "product_html" not in flask_app.blueprints:
        flask_app.register_blueprint(product_html)

    # 👉 Blueprint de páginas de VENTAS (el nuevo flujo registrar → confirmar → boleta)
    if "sale_html" not in flask_app.blueprints:
        flask_app.register_blueprint(sale_html)

    if "bp" not in flask_app.blueprints:
        flask_app.register_blueprint(bp)

    if "medical_bp" not in flask_app.blueprints:
        flask_app.register_blueprint(medical_bp)

    if "proveedor_bp" not in flask_app.blueprints:
        flask_app.register_blueprint(proveedor_bp)

    return flask_app
