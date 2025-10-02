from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from app.domain.use_cases.services.sale_service import SaleService
from app.domain.use_cases.product_use_cases import ProductUseCases
from app.infraestructure.repositories.sql_product_repository import SQLProductRepository
from app.infraestructure.utils.db import SessionLocal

sale_html = Blueprint('sale_html', __name__)
sale_service = SaleService()

@sale_html.route('/ventas', methods=['GET', 'POST'])
def ventas():
    if 'user_id' not in session or 'rol' not in session:
        return redirect(url_for('user_html.login'))
    try:
        if request.method == 'POST':
            producto_id = int(request.form['producto_id'])
            usuario_id = session.get('user_id')
            cantidad = int(request.form['cantidad'])
            total = float(request.form['total'])
            cliente = request.form.get('cliente')
            try:
                sale = sale_service.register_sale(producto_id, usuario_id, cantidad, total, cliente)
                if sale:
                    return redirect(url_for('sale_html.boleta', venta_id=sale.venta_id))
            except Exception as e:
                print(f"Error al registrar venta: {e}")
                flash('Ocurrió un error al registrar la venta. Intente más tarde.', 'danger')
            db_session = SessionLocal()
            try:
                product_repo = SQLProductRepository(db_session)
                product_use_cases = ProductUseCases(product_repo)
                products = product_use_cases.list_products()
                return render_template('registrar_venta.html', error='Error al registrar venta o stock insuficiente', products=products)
            except Exception as e:
                print(f"Error al cargar productos tras error de venta: {e}")
                flash('Ocurrió un error al cargar los productos. Intente más tarde.', 'danger')
                return render_template('registrar_venta.html', error='Error inesperado', products=[])
            finally:
                db_session.close()
        db_session = SessionLocal()
        try:
            product_repo = SQLProductRepository(db_session)
            product_use_cases = ProductUseCases(product_repo)
            products = product_use_cases.list_products()
            return render_template('registrar_venta.html', products=products)
        except Exception as e:
            print(f"Error al cargar productos: {e}")
            flash('Ocurrió un error al cargar los productos. Intente más tarde.', 'danger')
            return render_template('registrar_venta.html', error='Error inesperado', products=[])
        finally:
            db_session.close()
    except Exception as e:
        print(f"Error general en ventas: {e}")
        flash('Ocurrió un error inesperado. Intente más tarde.', 'danger')
        return render_template('registrar_venta.html', error='Error inesperado', products=[])

@sale_html.route('/ventas/historial')
def historial_ventas():
    if 'user_id' not in session or 'rol' not in session:
        return redirect(url_for('user_html.login'))
    try:
        ventas = sale_service.get_all_sales()
        return render_template('historial_ventas.html', ventas=ventas)
    except Exception as e:
        print(f"Error al cargar historial de ventas: {e}")
        flash('Ocurrió un error al cargar el historial de ventas. Intente más tarde.', 'danger')
        return render_template('historial_ventas.html', ventas=[])

@sale_html.route('/ventas/boleta/<int:venta_id>')
def boleta(venta_id):
    if 'user_id' not in session or 'rol' not in session:
        return redirect(url_for('user_html.login'))
    try:
        venta = sale_service.get_sale(venta_id)
        return render_template('boleta.html', venta=venta)
    except Exception as e:
        print(f"Error al cargar boleta: {e}")
        flash('Ocurrió un error al cargar la boleta. Intente más tarde.', 'danger')
        return redirect(url_for('sale_html.ventas')) 