#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para verificar fichas clínicas directamente en la base de datos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.infraestructure.utils.db import SessionLocal

def check_fichas_in_db():
    """Verificar fichas clínicas en la base de datos"""
    print("🔍 VERIFICANDO FICHAS CLÍNICAS EN LA BASE DE DATOS")
    print("=" * 60)
    
    try:
        session = SessionLocal()
        try:
            # Verificar si existe la tabla fichas_clinicas
            from sqlalchemy import text
            result = session.execute(text("SELECT COUNT(*) FROM fichas_clinicas;"))
            total_fichas = result.scalar()
            
            print(f"📊 Total fichas clínicas en BD: {total_fichas}")
            
            if total_fichas > 0:
                # Mostrar las fichas existentes
                result = session.execute(text("""
                    SELECT 
                        ficha_id,
                        numero_consulta,
                        fecha_consulta,
                        motivo_consulta,
                        estado,
                        fecha_creacion
                    FROM fichas_clinicas 
                    ORDER BY fecha_creacion DESC
                    LIMIT 5;
                """))
                
                fichas = result.fetchall()
                
                print("\n🗂️ ÚLTIMAS 5 FICHAS CLÍNICAS:")
                print("-" * 60)
                for ficha in fichas:
                    print(f"ID: {ficha[0]} | Consulta: {ficha[1]} | Fecha: {ficha[2]}")
                    print(f"Motivo: {ficha[3]}")
                    print(f"Estado: {ficha[4]} | Creado: {ficha[5]}")
                    print("-" * 60)
            else:
                print("⚠️ No hay fichas clínicas en la base de datos")
                
            return total_fichas > 0
            
        finally:
            session.close()
            
    except Exception as e:
        print(f"❌ Error verificando fichas: {e}")
        return False

def check_controller_import():
    """Verificar si el controlador se puede importar"""
    print("\n🔍 VERIFICANDO IMPORTACIÓN DEL CONTROLADOR")
    print("=" * 60)
    
    try:
        # Intentar importar el controlador
        from adapters.input.flask_app.medical_routes import ficha_clinica_controller
        print("✅ Controlador ficha_clinica_controller importado correctamente")
        
        # Verificar si tiene el método get_all_fichas_clinicas
        if hasattr(ficha_clinica_controller, 'get_all_fichas_clinicas'):
            print("✅ Método get_all_fichas_clinicas encontrado")
            return True
        else:
            print("❌ Método get_all_fichas_clinicas NO encontrado")
            return False
            
    except ImportError as e:
        print(f"❌ Error importando controlador: {e}")
        return False

if __name__ == "__main__":
    print("🚀 DIAGNÓSTICO COMPLETO DE FICHAS CLÍNICAS")
    print("=" * 70)
    
    # 1. Verificar datos en BD
    has_fichas = check_fichas_in_db()
    
    # 2. Verificar controlador
    controller_ok = check_controller_import()
    
    print("\n" + "=" * 70)
    print("📊 RESUMEN DEL DIAGNÓSTICO:")
    print(f"   Fichas en BD: {'✅' if has_fichas else '❌'}")
    print(f"   Controlador: {'✅' if controller_ok else '❌'}")
    
    if has_fichas and controller_ok:
        print("\n🎯 RECOMENDACIÓN: Probar el endpoint directamente en el navegador:")
        print("   👉 http://127.0.0.1:5000/api/fichas-clinicas")
    elif has_fichas and not controller_ok:
        print("\n🔧 PROBLEMA: Hay fichas en la BD pero el controlador tiene problemas")
    elif not has_fichas:
        print("\n📝 PROBLEMA: No hay fichas clínicas en la base de datos para mostrar")