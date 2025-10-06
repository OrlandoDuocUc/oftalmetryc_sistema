#!/usr/bin/env python3
from app.infraestructure.utils.db import SessionLocal
from app.domain.models.paciente import PacienteMedico
from app.domain.models.cliente import Cliente

def check_database():
    session = SessionLocal()
    try:
        # Ver si hay pacientes médicos
        pacientes = session.query(PacienteMedico).all()
        print(f'=== PACIENTES MÉDICOS: {len(pacientes)} ===')
        
        for p in pacientes:
            print(f'ID: {p.paciente_medico_id}')
            print(f'Cliente ID: {p.cliente_id}')
            print(f'Ficha: {p.numero_ficha}')
            print(f'Estado: {p.estado}')
            print(f'Fecha registro: {p.fecha_registro} (tipo: {type(p.fecha_registro)})')
            
            if p.cliente:
                print(f'Cliente: {p.cliente.nombres} {p.cliente.ap_pat}')
                print(f'Cliente RUT: {p.cliente.rut}')
                if p.cliente.fecha_nacimiento:
                    print(f'Fecha nacimiento: {p.cliente.fecha_nacimiento} (tipo: {type(p.cliente.fecha_nacimiento)})')
            else:
                print('Cliente: None')
            print('---')
            
        # Ver clientes
        clientes = session.query(Cliente).all()
        print(f'\n=== CLIENTES: {len(clientes)} ===')
        
        for c in clientes:
            print(f'Cliente ID: {c.cliente_id}')
            print(f'Nombres: {c.nombres} {c.ap_pat}')
            print(f'RUT: {c.rut}')
            print(f'Estado: {c.estado}')
            print(f'Fecha nacimiento: {c.fecha_nacimiento}')
            print('---')
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    check_database()