"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import json

from app.infraestructure.utils.db import SessionLocal
from app.infraestructure.repositories.sql_product_repository import SQLProductRepository
from app.domain.use_cases.services.sale_service import SaleService

sale_html = Blueprint("sale_html", __name__)

sale_service = SaleService()

# Utilidad: cargar productos para el select del primer HTML
def _get_products_json():
    with SessionLocal() as db:
        repo = SQLProductRepository(db)
        productos = repo.get_all(include_deleted=False)
        data = []
        for p in productos:
            data.append({
                "producto_id": p.producto_id,
                "nombre": p.nombre,
                "precio_unitario": float(p.precio_unitario or 0),
            })
        return json.dumps(data, ensure_ascii=False)

# 1) GET: registrar venta (primer HTML)
@sale_html.route("/registrar-venta", methods=["GET"])
def registrar_venta_page():
    products_json = _get_products_json()
    return render_template("registrar_venta.html", products_json=products_json)

# 2) POST: revisar venta (segundo HTML) — guarda items en sesión y muestra el resumen
@sale_html.route("/revisar-venta", methods=["POST"])
def revisar_venta_page():
    try:
        pedido_items_str = request.form.get("pedido_items", "[]")
        items = json.loads(pedido_items_str) if pedido_items_str else []

        if not items:
            flash("Debes agregar al menos 1 producto antes de continuar.", "warning")
            return redirect(url_for("sale_html.registrar_venta_page"))

        total_general = sum(float(i.get("subtotal", 0)) for i in items)
        # Guarda en sesión para el paso final
        session["venta_items"] = items
        session["venta_total"] = total_general

        return render_template(
            "confirmar_venta.html",
            items=items,
            total_general=total_general
        )
    except Exception as e:
        flash(f"Error al revisar la venta: {e}", "danger")
        return redirect(url_for("sale_html.registrar_venta_page"))

# 3) POST: finalizar venta definitiva — AQUÍ VA EL BLOQUE DE cliente_data y el register_sale_from_cart
@sale_html.route("/finalizar-venta-definitiva", methods=["POST"])
def finalizar_venta_definitiva():
    try:
        # Recupera los items que dejamos guardados en la sesión en /revisar-venta
        items = session.get("venta_items", [])
        if not items:
            flash("No hay ítems cargados para finalizar la venta.", "warning")
            return redirect(url_for("sale_html.registrar_venta_page"))

        # Si usas login, obtén el usuario de la sesión; si no, usa 1 por defecto
        usuario_id = session.get("usuario_id", 1)

        # 👇 ESTE ES EL BLOQUE QUE TE MOSTRÉ SUELTO: va exactamente aquí
        cliente_data = {
            "rut": request.form.get("cliente_rut") or "",
            "nombres": request.form.get("cliente_nombres") or "",
            "ap_pat": request.form.get("cliente_ap_pat") or "",
            "ap_mat": request.form.get("cliente_ap_mat") or "",
            "telefono": request.form.get("cliente_telefono") or "",
            "email": request.form.get("cliente_email") or "",
            "direccion": request.form.get("cliente_direccion") or "",
        }
        metodo_pago = request.form.get("metodo_pago", "efectivo")

        venta_id = sale_service.register_sale_from_cart(
            cart_items=items,
            usuario_id=usuario_id,
            cliente_data=cliente_data,
            metodo_pago=metodo_pago
        )

        # Limpia los temporales de sesión
        session.pop("venta_items", None)
        session.pop("venta_total", None)

        return redirect(url_for("sale_html.boleta_page", venta_id=venta_id))

    except Exception as e:
        flash(f"Error al finalizar la venta definitiva: {e}", "danger")
        return redirect(url_for("sale_html.registrar_venta_page"))

# 4) GET: boleta (tercer HTML)
@sale_html.route("/boleta/<int:venta_id>", methods=["GET"])
def boleta_page(venta_id):
    venta = sale_service.get_sale_details_for_receipt(venta_id)
    if not venta:
        flash("Venta no encontrada.", "warning")
        return redirect(url_for("sale_html.registrar_venta_page"))
    return render_template("boleta.html", venta=venta)

# (Opcional) Historial
@sale_html.route("/historial-ventas", methods=["GET"])
def historial_ventas_page():
    try:
        ventas = sale_service.get_all_sales_with_details()
        return render_template("historial_ventas.html", ventas=ventas)
    except Exception as e:
        flash(f"Error al cargar el historial de ventas: {e}", "danger")
        return redirect(url_for("sale_html.registrar_venta_page"))

"""