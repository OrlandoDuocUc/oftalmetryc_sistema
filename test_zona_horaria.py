#!/usr/bin/env python3
"""
Script de prueba para verificar la zona horaria de Chile
"""

import sys
import os
from datetime import datetime, timezone, timedelta

# Agregar el directorio raíz al path para importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.infraestructure.utils.date_utils import (
    get_chile_datetime, 
    get_chile_date, 
    get_day_start_end_chile, 
    format_datetime_chile,
    convert_utc_to_chile
)
from app.infraestructure.utils.db import SessionLocal
from app.domain.models.sale import Sale

def test_zona_horaria():
    """Prueba las funciones de zona horaria"""
    print("=== PRUEBA DE ZONA HORARIA ===")
    
    # Obtener fecha y hora actual en Chile
    chile_now = get_chile_datetime()
    chile_date = get_chile_date()
    
    print(f"Fecha y hora actual en Chile: {chile_now}")
    print(f"Fecha actual en Chile: {chile_date}")
    print(f"Zona horaria: {chile_now.tzinfo}")
    
    # Obtener inicio y fin del día en Chile
    start_of_day, end_of_day = get_day_start_end_chile()
    print(f"\nInicio del día en Chile: {start_of_day}")
    print(f"Fin del día en Chile: {end_of_day}")
    
    # Comparar con UTC
    utc_now = datetime.now(timezone.utc)
    print(f"\nFecha y hora actual en UTC: {utc_now}")
    print(f"Diferencia con Chile: {chile_now - utc_now}")
    
    # Probar conversión de UTC a Chile
    chile_converted = convert_utc_to_chile(utc_now)
    print(f"UTC convertido a Chile: {chile_converted}")
    
    return chile_date, start_of_day, end_of_day

def test_ventas_chile():
    """Prueba las ventas usando zona horaria de Chile"""
    print("\n=== PRUEBA DE VENTAS CON ZONA HORARIA DE CHILE ===")
    
    try:
        db_session = SessionLocal()
        
        # Obtener fecha y rangos de Chile
        chile_date, start_of_day, end_of_day = test_zona_horaria()
        
        print(f"\nBuscando ventas entre:")
        print(f"  Inicio: {start_of_day}")
        print(f"  Fin: {end_of_day}")
        
        # Obtener ventas del día en Chile
        ventas_hoy = db_session.query(Sale).filter(
            Sale.fecha >= start_of_day,
            Sale.fecha < end_of_day
        ).all()
        
        print(f"\nVentas encontradas hoy en Chile: {len(ventas_hoy)}")
        
        # Mostrar detalles de cada venta
        total_calculado = 0
        for i, venta in enumerate(ventas_hoy, 1):
            print(f"\nVenta {i}:")
            print(f"  ID: {venta.venta_id}")
            print(f"  Fecha UTC: {venta.fecha}")
            print(f"  Fecha Chile: {format_datetime_chile(venta.fecha)}")
            print(f"  Total: {venta.total}")
            
            if venta.total is not None:
                total_calculado += float(venta.total)
        
        print(f"\n=== RESUMEN ===")
        print(f"Total de ventas del día en Chile: ${total_calculado:.2f}")
        
        # Comparar con el método anterior (UTC)
        from datetime import date
        hoy_utc = date.today()
        ventas_utc = db_session.query(Sale).filter(
            Sale.fecha >= datetime.combine(hoy_utc, datetime.min.time()),
            Sale.fecha < datetime.combine(hoy_utc, datetime.max.time())
        ).all()
        
        total_utc = sum(float(v.total) for v in ventas_utc if v.total is not None)
        print(f"\nComparación:")
        print(f"  Método UTC: {len(ventas_utc)} ventas - ${total_utc:.2f}")
        print(f"  Método Chile: {len(ventas_hoy)} ventas - ${total_calculado:.2f}")
        
        if len(ventas_utc) != len(ventas_hoy):
            print(f"  ⚠️  DIFERENCIA DETECTADA!")
            print(f"  Las ventas que están en UTC pero no en Chile:")
            for v in ventas_utc:
                if v not in ventas_hoy:
                    print(f"    - Venta {v.venta_id}: {v.fecha} (UTC) -> {format_datetime_chile(v.fecha)} (Chile)")
        
        db_session.close()
        
    except Exception as e:
        print(f"Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ventas_chile() 