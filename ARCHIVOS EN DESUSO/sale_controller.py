"""
from flask import Blueprint, render_template, redirect, url_for, request, session, flash, jsonify
from app.domain.use_cases.services.sale_service import SaleService
from app.domain.use_cases.product_use_cases import ProductUseCases
import json # Necesario para procesar los datos del carrito

# Se crea UNA SOLA instancia de los servicios para todo el controlador.
sale_service = SaleService()
product_use_cases = ProductUseCases()

sale_html = Blueprint('sale_html', __name__)

# --- Rutas para Páginas HTML ---

@sale_html.route('/registrar-venta')
def registrar_venta_page():
    if 'user_id' not in session:
        return redirect(url_for('user_html.login'))
    
    try:
        # La página necesita la lista de productos para los selectores dinámicos.
        productos = product_use_cases.list_products()
        # Convertimos los productos a un formato JSON para que JavaScript pueda usarlos fácilmente.
        # Es importante manejar el caso en que un producto no tenga todos los atributos
        products_list = []
        for p in productos:
            product_dict = {
                'producto_id': p.producto_id,
                'nombre': p.nombre,
                'precio_unitario': float(p.precio_unitario) if p.precio_unitario is not None else 0.0,
                'stock': p.stock
            }
            products_list.append(product_dict)
        
        products_json = json.dumps(products_list)
        return render_template('registrar_venta.html', products=productos, products_json=products_json)
    except Exception as e:
        print(f"Error al cargar la página de registro de venta: {e}")
        flash('No se pudieron cargar los productos. Intente de nuevo.', 'danger')
        return render_template('registrar_venta.html', products=[], products_json='[]')

# --- NUEVA RUTA PARA LA PÁGINA DE CONFIRMACIÓN ---
@sale_html.route('/revisar-venta', methods=['POST'])
def revisar_venta_page():
    if 'user_id' not in session:
        return redirect(url_for('user_html.login'))

    # Los datos del pedido vienen en un campo oculto del formulario
    pedido_items_json = request.form.get('pedido_items')
    if not pedido_items_json:
        flash('El carrito está vacío.', 'warning')
        return redirect(url_for('sale_html.registrar_venta_page'))

    pedido_items = json.loads(pedido_items_json)
    total_general = sum(item['subtotal'] for item in pedido_items)

    # Guardamos el pedido en la sesión para usarlo en el paso final
    session['pedido_actual'] = pedido_items

    return render_template('confirmar_venta.html', items=pedido_items, total_general=total_general)


@sale_html.route('/historial-ventas')
def historial_ventas_page():
    if 'user_id' not in session:
        return redirect(url_for('user_html.login'))
    try:
        ventas = sale_service.get_all_sales_with_details()
        return render_template('historial_ventas.html', ventas=ventas)
    except Exception as e:
        print(f"Error al cargar el historial de ventas: {e}")
        flash('Ocurrió un error al cargar el historial.', 'danger')
        return render_template('historial_ventas.html', ventas=[])


@sale_html.route('/boleta/<int:venta_id>')
def boleta_page(venta_id):
    if 'user_id' not in session:
        return redirect(url_for('user_html.login'))
    try:
        venta = sale_service.get_sale_details_for_receipt(venta_id)
        if not venta:
            flash('Venta no encontrada.', 'danger')
            return redirect(url_for('sale_html.historial_ventas_page'))
        return render_template('boleta.html', venta=venta)
    except Exception as e:
        print(f"Error al generar la boleta: {e}")
        flash('Error al generar la boleta.', 'danger')
        return redirect(url_for('sale_html.historial_ventas_page'))


# --- NUEVA RUTA PARA FINALIZAR LA VENTA DESDE LA PÁGINA DE CONFIRMACIÓN ---
@sale_html.route('/finalizar-venta-definitiva', methods=['POST'])
def finalizar_venta_definitiva():
    if 'user_id' not in session or not session.get('pedido_actual'):
        flash('La sesión ha expirado o no hay un pedido que procesar.', 'danger')
        return redirect(url_for('user_html.login'))

    try:
        # Los datos del cliente vienen del formulario de la página de confirmación
        cliente_data = {
            'nombres': request.form.get('cliente_nombres'),
            'ap_pat': request.form.get('cliente_ap_pat'),
            'ap_mat': request.form.get('cliente_ap_mat'),
            'telefono': request.form.get('cliente_telefono'),
            'email': request.form.get('cliente_email')
        }
        
        # El pedido lo recuperamos de la sesión
        pedido_items = session['pedido_actual']

        # Llamamos al servicio para registrar todo
        primera_venta_id = sale_service.register_sale_from_cart(
            cart_items=pedido_items,
            usuario_id=session['user_id'],
            cliente_data=cliente_data
        )

        # Limpiamos la sesión después de una venta exitosa
        session.pop('pedido_actual', None)

        if primera_venta_id:
            flash('Venta registrada exitosamente.', 'success')
            return redirect(url_for('sale_html.boleta_page', venta_id=primera_venta_id))
        else:
            raise Exception("No se pudo registrar la venta.")

    except Exception as e:
        print(f"Error al finalizar la venta definitiva: {e}")
        flash(f'Ocurrió un error al procesar la venta: {str(e)}', 'danger')
        return redirect(url_for('sale_html.registrar_venta_page'))

"""