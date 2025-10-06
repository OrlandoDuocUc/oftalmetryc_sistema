#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de depuración para el API de pacientes médicos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.infraestructure.utils.db import SessionLocal
from app.domain.models.paciente import PacienteMedico
from app.domain.models.cliente import Cliente
from sqlalchemy.orm import joinedload
import traceback

def test_get_pacientes():
    """Prueba el método get_all_pacientes_medicos directamente"""
    print("🔍 Iniciando prueba de GET pacientes médicos...")
    
    try:
        session = SessionLocal()
        try:
            print("✅ Conexión a base de datos establecida")
            
            # Probar consulta simple primero
            print("\n1️⃣ Probando consulta simple...")
            pacientes_count = session.query(PacienteMedico).count()
            print(f"✅ Total pacientes médicos: {pacientes_count}")
            
            # Probar consulta con joinedload
            print("\n2️⃣ Probando consulta con joinedload...")
            pacientes_medicos = session.query(PacienteMedico)\
                .options(joinedload(PacienteMedico.cliente))\
                .filter(PacienteMedico.estado == True)\
                .all()
            
            print(f"✅ Pacientes médicos activos: {len(pacientes_medicos)}")
            
            # Probar to_dict en cada paciente
            print("\n3️⃣ Probando to_dict() en cada paciente...")
            for i, pm in enumerate(pacientes_medicos):
                try:
                    print(f"   Paciente {i+1}:")
                    print(f"   - ID: {pm.paciente_medico_id}")
                    print(f"   - Número ficha: {pm.numero_ficha}")
                    print(f"   - Cliente ID: {pm.cliente_id}")
                    print(f"   - Estado: {pm.estado}")
                    
                    # Probar to_dict
                    data = pm.to_dict()
                    print(f"   ✅ to_dict() exitoso")
                    
                    # Verificar cliente
                    if pm.cliente:
                        print(f"   - Cliente: {pm.cliente.nombres} {pm.cliente.ap_pat}")
                    else:
                        print(f"   ❌ Cliente es None")
                        
                except Exception as e:
                    print(f"   ❌ Error en paciente {i+1}: {str(e)}")
                    traceback.print_exc()
            
            return True
            
        finally:
            session.close()
            
    except Exception as e:
        print(f"❌ Error general: {str(e)}")
        traceback.print_exc()
        return False

def test_create_simple_patient():
    """Prueba crear un paciente simple directamente"""
    print("\n🆕 Probando creación directa de paciente...")
    
    try:
        session = SessionLocal()
        try:
            # 1. Crear cliente
            nuevo_cliente = Cliente(
                nombres="Juan",
                ap_pat="Pérez",
                ap_mat="González",
                rut="12.345.678-9",
                email="juan@test.com",
                telefono="+56912345678",
                estado=True
            )
            
            session.add(nuevo_cliente)
            session.flush()
            print(f"✅ Cliente creado con ID: {nuevo_cliente.cliente_id}")
            
            # 2. Crear paciente médico
            nuevo_paciente = PacienteMedico(
                cliente_id=nuevo_cliente.cliente_id,
                numero_ficha="FM-TEST-001",
                antecedentes_medicos="Test",
                estado=True
            )
            
            session.add(nuevo_paciente)
            session.commit()
            session.refresh(nuevo_paciente)
            print(f"✅ Paciente médico creado con ID: {nuevo_paciente.paciente_medico_id}")
            
            # 3. Probar to_dict
            data = nuevo_paciente.to_dict()
            print(f"✅ to_dict() exitoso: {data}")
            
            return True
            
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            
    except Exception as e:
        print(f"❌ Error creando paciente: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO DEPURACIÓN DEL API DE PACIENTES MÉDICOS")
    print("=" * 60)
    
    # Ejecutar pruebas
    test1 = test_get_pacientes()
    test2 = test_create_simple_patient()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS:")
    print(f"   GET pacientes: {'✅' if test1 else '❌'}")
    print(f"   CREATE paciente: {'✅' if test2 else '❌'}")
    
    if test1 and test2:
        print("🎉 ¡Todas las pruebas pasaron!")
    else:
        print("⚠️ Hay problemas que requieren atención")