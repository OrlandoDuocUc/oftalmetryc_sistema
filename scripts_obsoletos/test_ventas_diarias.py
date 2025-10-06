#!/usr/bin/env python3
"""
Script de prueba para verificar el cálculo de ventas diarias en el dashboard
"""

import sys
import os
from datetime import datetime, date, timedelta
from decimal import Decimal

# Agregar el directorio raíz al path para importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.infraestructure.utils.db import SessionLocal
from app.domain.models.sale import Sale
from app.domain.models.products import Product
from app.domain.models.cliente import Cliente

def test_ventas_diarias():
    """Prueba el cálculo de ventas del día actual"""
    print("=== PRUEBA DE VENTAS DIARIAS ===")
    
    try:
        db_session = SessionLocal()
        
        # Obtener la fecha actual
        hoy = date.today()
        print(f"Fecha actual: {hoy}")
        
        # Obtener todas las ventas del día actual
        ventas_hoy = db_session.query(Sale).filter(
            Sale.fecha >= datetime.combine(hoy, datetime.min.time()),
            Sale.fecha < datetime.combine(hoy, datetime.max.time())
        ).all()
        
        print(f"Total de ventas encontradas hoy: {len(ventas_hoy)}")
        
        # Mostrar detalles de cada venta
        total_calculado = 0
        for i, venta in enumerate(ventas_hoy, 1):
            print(f"\nVenta {i}:")
            print(f"  ID: {venta.venta_id}")
            print(f"  Fecha: {venta.fecha}")
            print(f"  Total: {venta.total}")
            print(f"  Cantidad: {venta.cantidad}")
            print(f"  Producto ID: {venta.producto_id}")
            print(f"  Cliente ID: {venta.cliente_id}")
            
            # Verificar si el total es válido
            if venta.total is not None:
                total_calculado += float(venta.total)
                print(f"  Total válido: Sí")
            else:
                print(f"  Total válido: No (None)")
        
        print(f"\n=== RESUMEN ===")
        print(f"Total de ventas del día: ${total_calculado:.2f}")
        
        # Verificar también las ventas de los últimos 7 días
        print(f"\n=== VENTAS DE LOS ÚLTIMOS 7 DÍAS ===")
        for i in range(7):
            fecha = hoy - timedelta(days=i)
            ventas_fecha = db_session.query(Sale).filter(
                Sale.fecha >= datetime.combine(fecha, datetime.min.time()),
                Sale.fecha < datetime.combine(fecha, datetime.max.time())
            ).all()
            
            total_fecha = sum(float(v.total) for v in ventas_fecha if v.total is not None)
            print(f"{fecha.strftime('%d/%m/%Y')}: {len(ventas_fecha)} ventas - ${total_fecha:.2f}")
        
        # Verificar si hay ventas con total None o 0
        ventas_problematicas = db_session.query(Sale).filter(
            (Sale.total.is_(None)) | (Sale.total == 0)
        ).all()
        
        if ventas_problematicas:
            print(f"\n=== VENTAS CON PROBLEMAS ===")
            print(f"Se encontraron {len(ventas_problematicas)} ventas con total None o 0:")
            for venta in ventas_problematicas:
                print(f"  Venta ID: {venta.venta_id}, Total: {venta.total}, Fecha: {venta.fecha}")
        
        db_session.close()
        
    except Exception as e:
        print(f"Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()

def test_dashboard_calculation():
    """Prueba el cálculo exacto que usa el dashboard"""
    print("\n=== PRUEBA DEL CÁLCULO DEL DASHBOARD ===")
    
    try:
        db_session = SessionLocal()
        
        # Obtener productos en stock (stock > 0)
        productos_en_stock = db_session.query(Product).filter(Product.stock > 0).count()
        print(f"Productos en stock: {productos_en_stock}")
        
        # Obtener ventas del día actual (mismo código que el dashboard)
        hoy = date.today()
        ventas_hoy = db_session.query(Sale).filter(
            Sale.fecha >= datetime.combine(hoy, datetime.min.time()),
            Sale.fecha < datetime.combine(hoy, datetime.max.time())
        ).all()
        
        # Calcular total de ventas del día (mismo código que el dashboard)
        total_ventas_hoy = sum(float(venta.total) for venta in ventas_hoy if venta.total is not None)
        
        print(f"Ventas del día: {len(ventas_hoy)}")
        print(f"Total ventas del día: ${total_ventas_hoy:.2f}")
        
        # Verificar cada venta individualmente
        print(f"\nDetalle de ventas del día:")
        for i, venta in enumerate(ventas_hoy, 1):
            total_venta = float(venta.total) if venta.total is not None else 0
            print(f"  {i}. Venta {venta.venta_id}: ${total_venta:.2f}")
        
        db_session.close()
        
    except Exception as e:
        print(f"Error durante la prueba del dashboard: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ventas_diarias()
    test_dashboard_calculation() 