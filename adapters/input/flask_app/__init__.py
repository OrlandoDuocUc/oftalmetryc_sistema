# adapters/input/flask_app/__init__.py

from flask import Flask
import os
from adapters.input.flask_app.controllers.user_controller import user_html
from adapters.input.flask_app.controllers.product_controller import product_html
from adapters.input.flask_app.controllers.sale_controller import sale_html
from .routes import bp  # Agregar la importación del blueprint principal
from .medical_routes import medical_bp  # Importar las rutas médicas (incluye ficha clínica)
from app.infraestructure.utils.currency_utils import format_currency_simple
from config.settings import config_by_name

def create_app(config_name='development'):
    # Obtener configuración según el entorno
    config_class = config_by_name.get(config_name, config_by_name['development'])
    
    base_dir = os.path.abspath(os.path.dirname(__file__))
    template_folder = os.path.join(base_dir, 'templates')
    static_folder = os.path.join(base_dir, 'static')
    
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    
    # Aplicar configuración
    app.config.from_object(config_class)
    
    # Registrar filtro personalizado para formatear moneda
    app.jinja_env.filters['currency'] = format_currency_simple
    
    # Registrar blueprints
    app.register_blueprint(user_html)
    app.register_blueprint(product_html)
    app.register_blueprint(sale_html)
    app.register_blueprint(bp)  # Registrar el blueprint principal con todas las rutas
    app.register_blueprint(medical_bp)  # Registrar las rutas médicas (incluye ficha clínica)
    
    return app
