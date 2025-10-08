from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from app.domain.use_cases.product_use_cases import ProductUseCases
from app.domain.use_cases.services.sale_service import SaleService

product_html = Blueprint('product_html', __name__)

# Se crea UNA SOLA instancia del servicio para todo el controlador.
product_use_cases = ProductUseCases()
sale_service = SaleService()

@product_html.route('/dashboard') # La ruta '/' es ambigua, es mejor usar '/dashboard'
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('user_html.login'))
    
    try:
        # La lógica del dashboard ahora debería estar idealmente en su propio servicio.
        # Por ahora, la mantenemos aquí pero simplificada.
        stats = sale_service.get_dashboard_stats()
        
        return render_template('dashboard.html', 
                               stock_total_productos=stats.get('total_stock', 0), 
                               productos_bajo_stock=stats.get('productos_stock_bajo', []), 
                               total_ventas_hoy=stats.get('total_ventas_hoy', 0), 
                               ventas_recientes=stats.get('ventas_recientes', []), 
                               pagos_pendientes=0)
    except Exception as e:
        print(f"Error en dashboard: {e}")
        flash('Ocurrió un error al cargar el dashboard.', 'danger')
        return render_template('dashboard.html', stock_total_productos=0, productos_bajo_stock=[], total_ventas_hoy=0, ventas_recientes=[], pagos_pendientes=0)

@product_html.route('/productos', methods=['GET', 'POST'])
def productos():
    if session.get('rol', '').lower() != 'administrador':
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('user_html.login'))
        
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            # Convertir a tipos correctos
            data['stock'] = int(data.get('stock', 0))
            data['precio_unitario'] = float(data.get('precio_unitario', 0.0))
            
            product_use_cases.create_product(data)
            flash('Producto creado exitosamente.', 'success')
        except Exception as e:
            print(f"Error al crear producto: {e}")
            flash(f'Ocurrió un error al crear el producto: {e}', 'danger')
        return redirect(url_for('product_html.productos'))

    # Método GET
    try:
        products = product_use_cases.list_products()
        return render_template('productos.html', products=products)
    except Exception as e:
        print(f"Error al listar productos: {e}")
        flash('Ocurrió un error al cargar los productos.', 'danger')
        return render_template('productos.html', products=[])

@product_html.route('/productos/eliminados')
def productos_eliminados():
    if session.get('rol', '').lower() != 'administrador':
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('user_html.login'))

    try:
        deleted_products = product_use_cases.list_deleted_products()
        return render_template('productos.html', products=[], deleted_products=deleted_products)
    except Exception as e:
        print(f"Error al listar productos eliminados: {e}")
        flash('Ocurrió un error al cargar los productos eliminados.', 'danger')
        return render_template('productos.html', products=[], deleted_products=[])

@product_html.route('/productos/edit/<int:product_id>', methods=['POST'])
def editar_producto(product_id):
    if session.get('rol', '').lower() != 'administrador':
        return redirect(url_for('user_html.login'))
    try:
        data = request.form.to_dict()
        data['stock'] = int(data.get('stock', 0))
        data['precio_unitario'] = float(data.get('precio_unitario', 0.0))
        
        product_use_cases.update_product(product_id, data)
        flash('Producto actualizado correctamente.', 'success')
    except Exception as e:
        print(f"Error al editar producto: {e}")
        flash(f'Ocurrió un error al editar el producto: {e}', 'danger')
    return redirect(url_for('product_html.productos'))

@product_html.route('/productos/delete/<int:product_id>', methods=['POST'])
def eliminar_producto(product_id):
    if session.get('rol', '').lower() != 'administrador':
        return redirect(url_for('user_html.login'))
    try:
        success = product_use_cases.delete_product(product_id)
        if success:
             flash('Producto eliminado físicamente.', 'success')
        else:
             flash('El producto no se eliminó físicamente (puede tener ventas asociadas) y fue desactivado.', 'warning')
    except Exception as e:
        print(f"Error al eliminar producto: {e}")
        flash('Ocurrió un error al eliminar el producto.', 'danger')
    return redirect(url_for('product_html.productos'))

@product_html.route('/productos/restore/<int:product_id>', methods=['POST'])
def restaurar_producto(product_id):
    if session.get('rol', '').lower() != 'administrador':
        return redirect(url_for('user_html.login'))
    try:
        product_use_cases.restore_product(product_id)
        flash('Producto restaurado exitosamente.', 'success')
    except Exception as e:
        print(f"Error al restaurar producto: {e}")
        flash('Ocurrió un error al restaurar el producto.', 'danger')
    return redirect(url_for('product_html.productos_eliminados'))
