# adapters/input/flask_app/__init__.py

import os
from flask import Flask
from config.settings import config_by_name
from app.infraestructure.utils.currency_utils import format_currency_simple

# 👉 Importa la instancia global de SQLAlchemy que ya tienes
from app.infraestructure.utils.db import db, DATABASE_URL

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
    # Config base
    config_class = config_by_name.get(config_name, config_by_name["development"])

    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_folder = os.path.join(base_dir, "templates")
    static_folder = os.path.join(base_dir, "static")

    # ⚠️ Nombre 'flask_app' para no chocar con el paquete 'app'
    flask_app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    flask_app.config.from_object(config_class)

    # SECRET_KEY (necesaria por uso de session en flujo de venta)
    if not flask_app.config.get("SECRET_KEY"):
        flask_app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")

    # Evitar warning y consumo extra de memoria
    flask_app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)

    # Si la URI no viene de la config, toma la de DATABASE_URL (Render/local)
    if not flask_app.config.get("SQLALCHEMY_DATABASE_URI") and DATABASE_URL:
        flask_app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

    # Para recargar plantillas en dev (opcional)
    flask_app.config.setdefault("TEMPLATES_AUTO_RELOAD", True)

    # Filtro de moneda usado en tus templates: {{ valor|currency }}
    flask_app.jinja_env.filters["currency"] = format_currency_simple

    # ────────────── SQLAlchemy: bind de la app ──────────────
    # MUY IMPORTANTE: con esto db.session queda atado a la app
    db.init_app(flask_app)

    # Autocommit por request:
    # - Si no hubo excepción -> commit
    # - Si hubo -> rollback
    @flask_app.teardown_request
    def _auto_commit_teardown(exc):
        try:
            if exc is None:
                db.session.commit()
            else:
                db.session.rollback()
        except Exception:
            # si commit falla, aseguremos rollback y propagamos
            db.session.rollback()
            raise
        finally:
            # siempre limpia el session context
            db.session.remove()

    # ────────────── Registro de Blueprints (evita doble registro) ──────────────
    if "user_html" not in flask_app.blueprints:
        flask_app.register_blueprint(user_html)

    if "product_html" not in flask_app.blueprints:
        flask_app.register_blueprint(product_html)

    # 👉 Blueprint de páginas de VENTAS (nuevo flujo registrar → confirmar → boleta)
    if "sale_html" not in flask_app.blueprints:
        flask_app.register_blueprint(sale_html)

    if "bp" not in flask_app.blueprints:
        flask_app.register_blueprint(bp)

    if "medical_bp" not in flask_app.blueprints:
        flask_app.register_blueprint(medical_bp)

    if "proveedor_bp" not in flask_app.blueprints:
        flask_app.register_blueprint(proveedor_bp)

    return flask_app
