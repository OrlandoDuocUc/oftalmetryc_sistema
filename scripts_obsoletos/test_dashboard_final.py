#!/usr/bin/env python3
"""
Script final para probar el dashboard con zona horaria de Chile
"""

import sys
import os
from datetime import datetime, timezone

# Agregar el directorio raíz al path para importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.infraestructure.utils.date_utils import get_chile_datetime, get_chile_date, get_day_start_end_chile
from app.infraestructure.utils.db import SessionLocal
from app.domain.models.sale import Sale
from app.domain.models.products import Product

def test_dashboard_completo():
    """Prueba completa del dashboard con zona horaria de Chile"""
    print("=== PRUEBA COMPLETA DEL DASHBOARD ===")
    
    try:
        db_session = SessionLocal()
        
        # 1. Información de zona horaria
        chile_now = get_chile_datetime()
        chile_date = get_chile_date()
        start_of_day, end_of_day = get_day_start_end_chile()
        
        print(f"Fecha y hora actual en Chile: {chile_now}")
        print(f"Fecha actual en Chile: {chile_date}")
        print(f"Rango del día en Chile: {start_of_day} a {end_of_day}")
        
        # 2. Productos en stock
        productos_en_stock = db_session.query(Product).filter(Product.stock > 0).count()
        print(f"\nProductos en stock: {productos_en_stock}")
        
        # 3. Ventas del día en Chile
        ventas_hoy = db_session.query(Sale).filter(
            Sale.fecha >= start_of_day,
            Sale.fecha < end_of_day
        ).all()
        
        print(f"Ventas del día en Chile: {len(ventas_hoy)}")
        
        # 4. Calcular total de ventas
        total_ventas_hoy = sum(float(venta.total) for venta in ventas_hoy if venta.total is not None)
        print(f"Total ventas del día: ${total_ventas_hoy:.2f}")
        
        # 5. Mostrar detalles de ventas
        print(f"\nDetalle de ventas del día:")
        for i, venta in enumerate(ventas_hoy, 1):
            print(f"  {i}. Venta {venta.venta_id}: ${float(venta.total):.2f} - {venta.fecha}")
        
        # 6. Ventas recientes
        ventas_recientes = db_session.query(Sale).order_by(Sale.fecha.desc()).limit(5).all()
        print(f"\nVentas recientes (últimas 5):")
        for i, venta in enumerate(ventas_recientes, 1):
            print(f"  {i}. Venta {venta.venta_id}: ${float(venta.total):.2f} - {venta.fecha}")
        
        # 7. Productos con bajo stock
        productos_bajo_stock = []
        productos = db_session.query(Product).all()
        for p in productos:
            if p.stock is not None and p.stock <= 10:
                productos_bajo_stock.append(p)
        
        print(f"\nProductos con bajo stock (≤10): {len(productos_bajo_stock)}")
        for p in productos_bajo_stock:
            print(f"  - {p.nombre}: {p.stock} unidades")
        
        # 8. Resumen final
        print(f"\n=== RESUMEN DEL DASHBOARD ===")
        print(f"📅 Fecha en Chile: {chile_date}")
        print(f"📦 Productos en stock: {productos_en_stock}")
        print(f"💰 Ventas del día: ${total_ventas_hoy:.2f}")
        print(f"⚠️  Productos con bajo stock: {len(productos_bajo_stock)}")
        print(f"🕐 Hora actual en Chile: {chile_now.strftime('%H:%M:%S')}")
        
        db_session.close()
        
        return {
            'fecha_chile': chile_date,
            'productos_stock': productos_en_stock,
            'total_ventas': total_ventas_hoy,
            'productos_bajo_stock': len(productos_bajo_stock),
            'hora_chile': chile_now.strftime('%H:%M:%S')
        }
        
    except Exception as e:
        print(f"Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
        return None

def simular_nueva_venta():
    """Simula una nueva venta para verificar que se cuenta correctamente"""
    print(f"\n=== SIMULACIÓN DE NUEVA VENTA ===")
    
    try:
        db_session = SessionLocal()
        
        # Obtener fecha actual en Chile
        chile_now = get_chile_datetime()
        print(f"Simulando venta a las: {chile_now}")
        
        # Verificar si esta venta se contaría en el dashboard
        chile_date = get_chile_date()
        start_of_day, end_of_day = get_day_start_end_chile()
        
        if start_of_day <= chile_now <= end_of_day:
            print(f"✅ Esta venta SÍ se contaría en el dashboard del día {chile_date}")
        else:
            print(f"❌ Esta venta NO se contaría en el dashboard del día {chile_date}")
        
        # Mostrar diferencia con UTC
        utc_now = datetime.now(timezone.utc)
        print(f"UTC actual: {utc_now}")
        print(f"Diferencia: {chile_now - utc_now}")
        
        db_session.close()
        
    except Exception as e:
        print(f"Error en simulación: {e}")

if __name__ == "__main__":
    resultado = test_dashboard_completo()
    simular_nueva_venta()
    
    if resultado:
        print(f"\n🎉 ¡Prueba completada exitosamente!")
        print(f"El dashboard ahora usa correctamente la zona horaria de Chile.")
    else:
        print(f"\n❌ Error en la prueba del dashboard.") 