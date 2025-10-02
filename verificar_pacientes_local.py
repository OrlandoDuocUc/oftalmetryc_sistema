#!/usr/bin/env python3
"""
VERIFICADOR DE PACIENTES LOCAL
=============================

Verifica si los pacientes se están guardando correctamente
en la base de datos local para diagnosticar el problema.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.infraestructure.utils.db_session import get_db_session
from app.infraestructure.utils.models import Paciente

def verificar_pacientes_local():
    """Verifica pacientes en BD local"""
    
    print("🔍 VERIFICADOR DE PACIENTES - BASE DE DATOS LOCAL")
    print("=" * 55)
    
    try:
        # Obtener sesión de BD
        db = get_db_session()
        
        # Contar total pacientes
        total_pacientes = db.query(Paciente).count()
        print(f"👥 Total pacientes en BD local: {total_pacientes}")
        
        # Obtener últimos 5 pacientes
        ultimos_pacientes = db.query(Paciente).order_by(Paciente.created_at.desc()).limit(5).all()
        
        if ultimos_pacientes:
            print(f"\n📋 ÚLTIMOS 5 PACIENTES REGISTRADOS:")
            print("-" * 40)
            for paciente in ultimos_pacientes:
                print(f"🏷️ ID: {paciente.id}")
                print(f"🆔 RUT: {paciente.rut} | CI: {paciente.ci}")
                print(f"👤 Nombre: {paciente.nombre} {paciente.apellido}")
                print(f"📧 Email: {paciente.email}")
                print(f"📅 Creado: {paciente.created_at}")
                print("-" * 30)
        else:
            print("\n⚠️ NO HAY PACIENTES REGISTRADOS")
        
        # Verificar estructura de tabla
        print(f"\n🏗️ ESTRUCTURA DE TABLA PACIENTES:")
        print("-" * 40)
        for column in Paciente.__table__.columns:
            print(f"📋 {column.name}: {column.type}")
        
        db.close()
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def simular_busqueda_paciente():
    """Simula búsqueda de paciente como en ficha clínica"""
    
    print(f"\n🔍 SIMULANDO BÚSQUEDA DE PACIENTE:")
    print("-" * 40)
    
    try:
        db = get_db_session()
        
        # Buscar por diferentes criterios
        print("🔎 Búsqueda por RUT 'Test':")
        pacientes_rut = db.query(Paciente).filter(Paciente.rut.ilike('%Test%')).all()
        print(f"   Encontrados: {len(pacientes_rut)}")
        
        print("🔎 Búsqueda por nombre 'Juan':")
        pacientes_nombre = db.query(Paciente).filter(Paciente.nombre.ilike('%Juan%')).all()
        print(f"   Encontrados: {len(pacientes_nombre)}")
        
        print("🔎 Búsqueda por CI '12345':")
        pacientes_ci = db.query(Paciente).filter(Paciente.ci.ilike('%12345%')).all()
        print(f"   Encontrados: {len(pacientes_ci)}")
        
        db.close()
        
    except Exception as e:
        print(f"❌ ERROR en búsqueda: {str(e)}")

def diagnosticar_problema():
    """Diagnostica posibles problemas"""
    
    print(f"\n🎯 DIAGNÓSTICO DE PROBLEMAS POTENCIALES:")
    print("-" * 45)
    
    print("1️⃣ COMMIT DE TRANSACCIÓN:")
    print("   • Verificar que se hace db.commit() después de add()")
    print("   • Verificar manejo de excepciones")
    
    print("\n2️⃣ MODELO DE DATOS:")
    print("   • Confirmar que se usa el modelo correcto")
    print("   • Verificar importaciones")
    
    print("\n3️⃣ ENCODING:")
    print("   • Verificar caracteres especiales en RUT/CI")
    print("   • Confirmar encoding UTF-8")
    
    print("\n4️⃣ SESIÓN DE BD:")
    print("   • Verificar que se cierra correctamente")
    print("   • Confirmar conexión activa")

if __name__ == "__main__":
    verificar_pacientes_local()
    simular_busqueda_paciente()
    diagnosticar_problema()