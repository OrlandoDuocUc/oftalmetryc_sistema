from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from app.domain.use_cases.product_use_cases import ProductUseCases
from app.infraestructure.repositories.sql_product_repository import SQLProductRepository
from app.infraestructure.utils.db import SessionLocal
from app.domain.use_cases.services.sale_service import SaleService
from app.infraestructure.utils.date_utils import format_datetime_chile

product_html = Blueprint('product_html', __name__)

@product_html.route('/')
def dashboard():
    if 'user_id' not in session or 'rol' not in session:
        return redirect(url_for('user_html.login'))
    try:
        db_session = SessionLocal()
        product_repo = SQLProductRepository(db_session)
        product_use_cases = ProductUseCases(product_repo)
        sale_service = SaleService()
        stats = sale_service.get_dashboard_stats()
        products = product_use_cases.list_products()
        stock_total_productos = sum([int(getattr(p, 'stock', 0)) for p in products if getattr(p, 'stock', None) is not None])
        productos_bajo_stock = []
        for p in products:
            stock = getattr(p, 'stock', None)
            if stock is not None and int(stock) <= 10:
                productos_bajo_stock.append(p)
        total_ventas_hoy = stats['total_ventas_hoy']
        ventas_recientes = stats['ventas_recientes']
        pagos_pendientes = 0
        return render_template('dashboard.html', 
                             stock_total_productos=stock_total_productos, 
                             productos_bajo_stock=productos_bajo_stock, 
                             total_ventas_hoy=total_ventas_hoy, 
                             ventas_recientes=ventas_recientes, 
                             pagos_pendientes=pagos_pendientes)
    except Exception as e:
        print(f"Error en dashboard: {e}")
        flash('Ocurrió un error al cargar el dashboard. Intente más tarde.', 'danger')
        return render_template('dashboard.html', 
                             stock_total_productos=0, 
                             productos_bajo_stock=[], 
                             total_ventas_hoy=0, 
                             ventas_recientes=[], 
                             pagos_pendientes=0)
    finally:
        if 'db_session' in locals():
            db_session.close()

@product_html.route('/productos', methods=['GET', 'POST'])
def productos():
    if not session.get('user_id') or session.get('rol', '').lower() != 'administrador':
        return redirect(url_for('user_html.login'))
    try:
        db_session = SessionLocal()
        product_repo = SQLProductRepository(db_session)
        product_use_cases = ProductUseCases(product_repo)
        if request.method == 'POST':
            try:
                data = request.form.to_dict()
                campos_permitidos = ['nombre', 'descripcion', 'precio_unitario', 'stock']
                data = {k: v for k, v in data.items() if k in campos_permitidos}
                if 'stock' in data:
                    data['stock'] = int(data['stock'])
                if 'precio_unitario' in data:
                    data['precio_unitario'] = float(data['precio_unitario'])
                product_use_cases.create_product(data)
                return redirect(url_for('product_html.productos'))
            except Exception as e:
                print(f"Error al crear producto: {e}")
                flash('Ocurrió un error al crear el producto. Intente más tarde.', 'danger')
        try:
            products = product_use_cases.list_products()
        except Exception as e:
            print(f"Error al listar productos: {e}")
            flash('Ocurrió un error al cargar los productos. Intente más tarde.', 'danger')
            products = []
        return render_template('productos.html', products=products)
    except Exception as e:
        print(f"Error general en productos: {e}")
        flash('Ocurrió un error inesperado. Intente más tarde.', 'danger')
        return render_template('productos.html', products=[])
    finally:
        if 'db_session' in locals():
            db_session.close()

@product_html.route('/productos/eliminados')
def productos_eliminados():
    if 'user_id' not in session or 'rol' not in session:
        return redirect(url_for('user_html.login'))
    if session['rol'] != 'administrador':
        return redirect(url_for('product_html.productos'))
    try:
        db_session = SessionLocal()
        product_repo = SQLProductRepository(db_session)
        product_use_cases = ProductUseCases(product_repo)
        try:
            deleted_products = product_use_cases.list_deleted_products()
        except Exception as e:
            print(f"Error al listar productos eliminados: {e}")
            flash('Ocurrió un error al cargar los productos eliminados.', 'danger')
            deleted_products = []
        return render_template('productos.html', products=[], deleted_products=deleted_products)
    except Exception as e:
        print(f"Error general en productos eliminados: {e}")
        flash('Ocurrió un error inesperado. Intente más tarde.', 'danger')
        return render_template('productos.html', products=[], deleted_products=[])
    finally:
        if 'db_session' in locals():
            db_session.close()

@product_html.route('/productos/edit/<int:product_id>', methods=['POST'])
def editar_producto(product_id):
    if not session.get('user_id') or session.get('rol', '').lower() != 'administrador':
        return redirect(url_for('user_html.login'))
    try:
        db_session = SessionLocal()
        product_repo = SQLProductRepository(db_session)
        product_use_cases = ProductUseCases(product_repo)
        try:
            data = request.form.to_dict()
            campos_permitidos = ['nombre', 'descripcion', 'precio_unitario', 'stock']
            data = {k: v for k, v in data.items() if k in campos_permitidos}
            if 'stock' in data:
                data['stock'] = int(data['stock'])
            if 'precio_unitario' in data:
                data['precio_unitario'] = float(data['precio_unitario'])
            product_use_cases.update_product(product_id, data)
            return redirect(url_for('product_html.productos'))
        except Exception as e:
            print(f"Error al editar producto: {e}")
            flash('Ocurrió un error al editar el producto. Intente más tarde.', 'danger')
            return redirect(url_for('product_html.productos'))
    except Exception as e:
        print(f"Error general en editar producto: {e}")
        flash('Ocurrió un error inesperado. Intente más tarde.', 'danger')
        return redirect(url_for('product_html.productos'))
    finally:
        if 'db_session' in locals():
            db_session.close()

@product_html.route('/productos/delete/<int:product_id>', methods=['POST'])
def eliminar_producto(product_id):
    if not session.get('user_id') or session.get('rol', '').lower() != 'administrador':
        return redirect(url_for('user_html.login'))
    try:
        db_session = SessionLocal()
        product_repo = SQLProductRepository(db_session)
        product_use_cases = ProductUseCases(product_repo)
        try:
            product_use_cases.delete_product(product_id)
            return redirect(url_for('product_html.productos'))
        except Exception as e:
            print(f"Error al eliminar producto: {e}")
            flash('Ocurrió un error al eliminar el producto. Intente más tarde.', 'danger')
            return redirect(url_for('product_html.productos'))
    except Exception as e:
        print(f"Error general en eliminar producto: {e}")
        flash('Ocurrió un error inesperado. Intente más tarde.', 'danger')
        return redirect(url_for('product_html.productos'))
    finally:
        if 'db_session' in locals():
            db_session.close()

@product_html.route('/productos/restore/<int:product_id>', methods=['POST'])
def restaurar_producto(product_id):
    if 'user_id' not in session or 'rol' not in session or session['rol'] != 'administrador':
        return redirect(url_for('user_html.login'))
    try:
        db_session = SessionLocal()
        product_repo = SQLProductRepository(db_session)
        product_use_cases = ProductUseCases(product_repo)
        try:
            product_use_cases.restore_product(product_id)
            return redirect(url_for('product_html.productos_eliminados'))
        except Exception as e:
            print(f"Error al restaurar producto: {e}")
            flash('Ocurrió un error al restaurar el producto. Intente más tarde.', 'danger')
            return redirect(url_for('product_html.productos_eliminados'))
    except Exception as e:
        print(f"Error general en restaurar producto: {e}")
        flash('Ocurrió un error inesperado. Intente más tarde.', 'danger')
        return redirect(url_for('product_html.productos_eliminados'))
    finally:
        if 'db_session' in locals():
            db_session.close() 