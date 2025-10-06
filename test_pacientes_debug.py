#!/usr/bin/env python3
"""
Script de diagnóstico para probar la funcionalidad de pacientes médicos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.infraestructure.utils.db import SessionLocal
from app.domain.models.paciente import PacienteMedico
from app.domain.models.cliente import Cliente
from sqlalchemy.orm import joinedload
import traceback

def test_direct_query():
    """Test directo de consulta a la base de datos"""
    print("🔍 DIAGNÓSTICO: Consulta directa a pacientes_medicos")
    print("=" * 60)
    
    try:
        session = SessionLocal()
        
        # 1. Consultar clientes
        print("\n1. 📋 CLIENTES EN BASE DE DATOS:")
        clientes = session.query(Cliente).all()
        print(f"   Total clientes: {len(clientes)}")
        for cliente in clientes:
            print(f"   - ID: {cliente.cliente_id}, Nombre: {cliente.nombres} {cliente.ap_pat}, RUT: {cliente.rut}")
        
        # 2. Consultar pacientes médicos
        print("\n2. 🏥 PACIENTES MÉDICOS EN BASE DE DATOS:")
        pacientes = session.query(PacienteMedico).all()
        print(f"   Total pacientes médicos: {len(pacientes)}")
        for paciente in pacientes:
            print(f"   - ID: {paciente.paciente_medico_id}, Ficha: {paciente.numero_ficha}, Cliente ID: {paciente.cliente_id}")
        
        # 3. Probar JOIN como en el controlador
        print("\n3. 🔗 PROBANDO JOIN COMO EN EL CONTROLADOR:")
        pacientes_con_cliente = session.query(PacienteMedico)\
            .options(joinedload(PacienteMedico.cliente))\
            .filter(PacienteMedico.estado == True)\
            .all()
        
        print(f"   Total con JOIN: {len(pacientes_con_cliente)}")
        
        # 4. Probar to_dict() en cada paciente
        print("\n4. 📝 PROBANDO to_dict() EN CADA PACIENTE:")
        for i, pm in enumerate(pacientes_con_cliente):
            try:
                print(f"   Paciente {i+1}:")
                print(f"   - Número ficha: {pm.numero_ficha}")
                print(f"   - Cliente ID: {pm.cliente_id}")
                print(f"   - Cliente existe: {pm.cliente is not None}")
                if pm.cliente:
                    print(f"   - Cliente nombre: {pm.cliente.nombres}")
                
                # Probar to_dict()
                data = pm.to_dict()
                print(f"   - to_dict() funciona: ✅")
                print(f"   - Fecha registro: {data.get('fecha_registro')}")
                
            except Exception as e:
                print(f"   - ❌ ERROR en to_dict(): {str(e)}")
                traceback.print_exc()
        
        session.close()
        
    except Exception as e:
        print(f"❌ ERROR GENERAL: {str(e)}")
        traceback.print_exc()

def test_controller_simulation():
    """Simular exactamente lo que hace el controlador"""
    print("\n" + "=" * 60)
    print("🎭 SIMULANDO CONTROLADOR get_all_pacientes_medicos")
    print("=" * 60)
    
    try:
        session = SessionLocal()
        
        # Exactamente como en el controlador
        pacientes_medicos = session.query(PacienteMedico)\
            .options(joinedload(PacienteMedico.cliente))\
            .filter(PacienteMedico.estado == True)\
            .all()
        
        print(f"📊 Pacientes encontrados: {len(pacientes_medicos)}")
        
        result = []
        for pm in pacientes_medicos:
            try:
                # Simular to_dict()
                data = pm.to_dict()
                
                # Simular agregar datos del cliente
                if pm.cliente:
                    data['cliente'] = {
                        'nombres': pm.cliente.nombres,
                        'ap_pat': pm.cliente.ap_pat,
                        'ap_mat': pm.cliente.ap_mat,
                        'rut': pm.cliente.rut,
                        'email': pm.cliente.email,
                        'telefono': pm.cliente.telefono,
                        'direccion': pm.cliente.direccion,
                        'fecha_nacimiento': pm.cliente.fecha_nacimiento.isoformat() if pm.cliente.fecha_nacimiento else None
                    }
                
                result.append(data)
                print(f"✅ Paciente {pm.numero_ficha} procesado correctamente")
                
            except Exception as e:
                print(f"❌ ERROR procesando paciente {pm.numero_ficha}: {str(e)}")
                traceback.print_exc()
        
        print(f"\n📋 RESULTADO FINAL:")
        print(f"   - Pacientes procesados: {len(result)}")
        print(f"   - Datos de ejemplo: {result[0] if result else 'Sin datos'}")
        
        session.close()
        
    except Exception as e:
        print(f"❌ ERROR EN SIMULACIÓN: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 INICIANDO DIAGNÓSTICO DE PACIENTES MÉDICOS")
    test_direct_query()
    test_controller_simulation()
    print("\n✅ DIAGNÓSTICO COMPLETADO")