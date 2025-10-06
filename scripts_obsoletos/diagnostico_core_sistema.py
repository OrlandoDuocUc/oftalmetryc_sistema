#!/usr/bin/env python3
"""
DIAGNÓSTICO CORE - FUNCIONALIDADES CRÍTICAS
==========================================

Verifica las funcionalidades más importantes del sistema:
1. Creación de pacientes nuevos
2. Guardado de fichas clínicas
3. Visualización en historial consultas
4. Integridad de datos entre tablas

Este es el CORE del sistema médico.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verificar_core_sistema():
    """Verifica las funcionalidades core del sistema"""
    
    print("🔍 DIAGNÓSTICO CORE - FUNCIONALIDADES CRÍTICAS")
    print("=" * 55)
    
    try:
        from app.infraestructure.utils.db_session import get_db_session
        from app.infraestructure.utils.models import Paciente
        from app.domain.models.examen_basico import ExamenBasico
        
        db = get_db_session()
        
        print("\n👥 VERIFICANDO PACIENTES:")
        print("-" * 30)
        
        # Contar pacientes totales
        total_pacientes = db.query(Paciente).count()
        print(f"📊 Total pacientes en BD: {total_pacientes}")
        
        # Últimos 3 pacientes creados
        if total_pacientes > 0:
            ultimos_pacientes = db.query(Paciente).order_by(Paciente.created_at.desc()).limit(3).all()
            print(f"\n📋 ÚLTIMOS 3 PACIENTES CREADOS:")
            for i, paciente in enumerate(ultimos_pacientes, 1):
                print(f"  {i}. ID: {paciente.id} | RUT: {paciente.rut} | Nombre: {paciente.nombre} {paciente.apellido}")
                print(f"     📅 Creado: {paciente.created_at}")
        else:
            print("⚠️ NO HAY PACIENTES REGISTRADOS")
        
        print(f"\n🔬 VERIFICANDO FICHAS CLÍNICAS (EXÁMENES):")
        print("-" * 45)
        
        # Contar exámenes/fichas clínicas
        total_examenes = db.query(ExamenBasico).count()
        print(f"📊 Total fichas clínicas en BD: {total_examenes}")
        
        # Últimos 3 exámenes
        if total_examenes > 0:
            ultimos_examenes = db.query(ExamenBasico).order_by(ExamenBasico.fecha_examen.desc()).limit(3).all()
            print(f"\n📋 ÚLTIMAS 3 FICHAS CLÍNICAS CREADAS:")
            for i, examen in enumerate(ultimos_examenes, 1):
                print(f"  {i}. ID: {examen.id} | Paciente ID: {examen.paciente_id}")
                print(f"     📅 Fecha: {examen.fecha_examen}")
                print(f"     👁️ Agudeza OD: {examen.agudeza_visual_od or 'No registrada'}")
                print(f"     💊 Diagnóstico: {examen.diagnostico_principal or 'No registrado'}")
        else:
            print("⚠️ NO HAY FICHAS CLÍNICAS REGISTRADAS")
        
        print(f"\n🔗 VERIFICANDO RELACIÓN PACIENTES ↔ FICHAS:")
        print("-" * 45)
        
        # Verificar integridad entre pacientes y exámenes
        pacientes_con_fichas = db.query(Paciente.id).join(ExamenBasico, Paciente.id == ExamenBasico.paciente_id).distinct().count()
        pacientes_sin_fichas = total_pacientes - pacientes_con_fichas
        
        print(f"👥 Pacientes CON fichas clínicas: {pacientes_con_fichas}")
        print(f"👥 Pacientes SIN fichas clínicas: {pacientes_sin_fichas}")
        
        if pacientes_con_fichas > 0:
            print("\n📊 DETALLE PACIENTES CON FICHAS:")
            pacientes_detalle = db.execute("""
                SELECT p.id, p.nombre, p.apellido, COUNT(e.id) as total_fichas
                FROM pacientes p
                INNER JOIN examenes_basicos e ON p.id = e.paciente_id
                GROUP BY p.id, p.nombre, p.apellido
                ORDER BY total_fichas DESC
                LIMIT 5
            """).fetchall()
            
            for paciente in pacientes_detalle:
                print(f"  📋 {paciente[1]} {paciente[2]} → {paciente[3]} ficha(s) clínica(s)")
        
        db.close()
        
        return {
            'total_pacientes': total_pacientes,
            'total_examenes': total_examenes,
            'pacientes_con_fichas': pacientes_con_fichas
        }
        
    except Exception as e:
        print(f"❌ ERROR EN VERIFICACIÓN: {str(e)}")
        return None

def diagnosticar_problemas_historial():
    """Diagnostica por qué no aparecen fichas en historial"""
    
    print(f"\n🔍 DIAGNÓSTICO: ¿POR QUÉ NO APARECEN FICHAS EN HISTORIAL?")
    print("-" * 60)
    
    problemas_posibles = [
        "1️⃣ FICHAS INCOMPLETAS: Solo se muestran fichas 'finalizadas'",
        "2️⃣ FILTROS ACTIVOS: Hay filtros de fecha que ocultan fichas",
        "3️⃣ RELACIÓN BD: Problema foreign key paciente_id",
        "4️⃣ CONSULTA SQL: La query no trae todos los registros",
        "5️⃣ ESTADO FICHA: Campo 'estado' requiere valor específico",
        "6️⃣ PERMISOS: Usuario no tiene acceso a ciertas fichas"
    ]
    
    print("🎯 POSIBLES CAUSAS:")
    for problema in problemas_posibles:
        print(f"   {problema}")
    
    print(f"\n💡 SOLUCIÓN RECOMENDADA:")
    print("   • Verificar la consulta SQL en historial consultas")
    print("   • Revisar si hay campos requeridos para mostrar fichas")
    print("   • Confirmar que paciente_id se guarda correctamente")
    print("   • Verificar filtros de fecha en la interfaz")

def generar_plan_correccion():
    """Genera plan para corregir problemas identificados"""
    
    resultados = verificar_core_sistema()
    diagnosticar_problemas_historial()
    
    print(f"\n🛠️ PLAN DE CORRECCIÓN:")
    print("=" * 25)
    
    if resultados:
        if resultados['total_pacientes'] == 0:
            print("🔴 CRÍTICO: Sistema sin pacientes")
            print("   → Verificar funcionalidad crear paciente")
            
        if resultados['total_examenes'] == 0:
            print("🔴 CRÍTICO: Sistema sin fichas clínicas")
            print("   → Verificar funcionalidad guardar ficha")
            
        if resultados['total_pacientes'] > 0 and resultados['total_examenes'] == 0:
            print("🟡 PROBLEMA: Pacientes existen pero no hay fichas")
            print("   → Revisar proceso guardar ficha clínica")
            
        if resultados['total_examenes'] > 0 and resultados['pacientes_con_fichas'] == 0:
            print("🔴 CRÍTICO: Fichas existen pero sin relación a pacientes")
            print("   → Revisar foreign key paciente_id")
    
    print(f"\n📋 PRÓXIMOS PASOS:")
    print("1. Verificar consulta SQL en historial consultas")
    print("2. Revisar proceso de guardado de fichas clínicas")
    print("3. Confirmar relación pacientes ↔ fichas")
    print("4. Probar creación completa: paciente → ficha → historial")

if __name__ == "__main__":
    generar_plan_correccion()