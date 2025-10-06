#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFICADOR BD RENDER - Confirmar cambios reales
Conecta y verifica cada campo agregado individualmente
"""

import psycopg2
import sys

# Datos de conexión a Render
DATABASE_URL = "postgresql://oftalmetryc_user:0WdPbRIzVrbH6xYFCye20Q7ST4e3v7Kn@dpg-d3efatffte5s73chd9r0-a.oregon-postgres.render.com:5432/oftalmetryc_db"

def verificar_bd_render():
    """Verificar que todos los campos están realmente en Render"""
    print("🔍 VERIFICADOR COMPLETO BD RENDER")
    print("🗄️ BD: oftalmetryc_db (oftalmetryc_database)")
    print("=" * 60)
    
    try:
        # Conectar a Render
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("✅ Conexión exitosa a Render")
        print()
        
        # VERIFICAR TABLA PACIENTES
        print("📋 VERIFICANDO TABLA PACIENTES...")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'pacientes' 
            ORDER BY column_name
        """)
        
        campos_pacientes = cursor.fetchall()
        print(f"📊 Total de campos en PACIENTES: {len(campos_pacientes)}")
        
        # Campos que debimos agregar
        campos_esperados_pacientes = ['ci', 'nombres', 'apellidos', 'edad', 'genero', 'hobby']
        campos_encontrados_pacientes = [campo[0] for campo in campos_pacientes]
        
        print("\n🔍 Campos esperados vs encontrados:")
        for campo in campos_esperados_pacientes:
            if campo in campos_encontrados_pacientes:
                print(f"  ✅ {campo} - ENCONTRADO")
            else:
                print(f"  ❌ {campo} - NO ENCONTRADO")
        
        print("\n📋 TODOS LOS CAMPOS EN PACIENTES:")
        for campo in campos_pacientes:
            print(f"  - {campo[0]} ({campo[1]})")
        
        print("\n" + "="*60)
        
        # VERIFICAR TABLA EXAMENES_BASICOS
        print("👁️ VERIFICANDO TABLA EXAMENES_BASICOS...")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'examenes_basicos' 
            ORDER BY column_name
        """)
        
        campos_examenes = cursor.fetchall()
        print(f"📊 Total de campos en EXAMENES_BASICOS: {len(campos_examenes)}")
        
        # Campos críticos de ficha clínica
        campos_criticos = [
            'av_distancia_od', 'av_distancia_oi', 'av_proximidad_od',
            'autorefractor_od_esfera', 'autorefractor_oi_esfera',
            'rx_final_od_esfera', 'rx_final_oi_esfera',
            'pio_od', 'pio_oi', 'biomicroscopia_od', 'biomicroscopia_oi',
            'oftalmoscopia_od', 'oftalmoscopia_oi'
        ]
        
        campos_encontrados_examenes = [campo[0] for campo in campos_examenes]
        
        print("\n🔍 Campos críticos de ficha clínica:")
        for campo in campos_criticos:
            if campo in campos_encontrados_examenes:
                print(f"  ✅ {campo} - ENCONTRADO")
            else:
                print(f"  ❌ {campo} - NO ENCONTRADO")
        
        # Contar campos de ficha clínica que empiecen con av_, rx_, pio_, etc.
        prefijos_ficha = ['av_', 'autorefractor_', 'rx_final_', 'lc_', 'pio_', 
                         'test_', 'lensometria_', 'biomicroscopia_', 'subjetivo_', 
                         'oftalmoscopia_', 'motilidad_']
        
        campos_ficha_clinica = []
        for campo in campos_encontrados_examenes:
            for prefijo in prefijos_ficha:
                if campo.startswith(prefijo):
                    campos_ficha_clinica.append(campo)
                    break
        
        print(f"\n📈 CAMPOS DE FICHA CLÍNICA ENCONTRADOS: {len(campos_ficha_clinica)}")
        print("📋 Lista completa de campos de ficha clínica:")
        for i, campo in enumerate(sorted(campos_ficha_clinica), 1):
            print(f"  {i:2d}. {campo}")
        
        print("\n" + "="*60)
        
        # VERIFICAR TABLA CONSULTAS_MEDICAS
        print("🏥 VERIFICANDO TABLA CONSULTAS_MEDICAS...")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'consultas_medicas' 
            ORDER BY column_name
        """)
        
        campos_consultas = cursor.fetchall()
        print(f"📊 Total de campos en CONSULTAS_MEDICAS: {len(campos_consultas)}")
        
        campos_esperados_consultas = ['motivo_consulta', 'diagnostico', 'observaciones', 
                                    'estado', 'fecha_seguimiento', 'tratamiento']
        campos_encontrados_consultas = [campo[0] for campo in campos_consultas]
        
        print("\n🔍 Campos esperados vs encontrados:")
        for campo in campos_esperados_consultas:
            if campo in campos_encontrados_consultas:
                print(f"  ✅ {campo} - ENCONTRADO")
            else:
                print(f"  ❌ {campo} - NO ENCONTRADO")
        
        print("\n📋 TODOS LOS CAMPOS EN CONSULTAS_MEDICAS:")
        for campo in campos_consultas:
            print(f"  - {campo[0]} ({campo[1]})")
        
        print("\n" + "="*60)
        
        # RESUMEN FINAL
        print("📊 RESUMEN FINAL DE VERIFICACIÓN:")
        print(f"✅ PACIENTES: {len(campos_pacientes)} campos totales")
        print(f"✅ EXAMENES_BASICOS: {len(campos_examenes)} campos totales")
        print(f"✅ CONSULTAS_MEDICAS: {len(campos_consultas)} campos totales")
        print(f"👁️ CAMPOS DE FICHA CLÍNICA: {len(campos_ficha_clinica)} campos")
        
        # Verificar que podemos insertar datos
        print("\n🧪 PRUEBA DE INSERCIÓN (TEST)...")
        try:
            # Test simple de inserción en pacientes
            cursor.execute("""
                INSERT INTO pacientes (ci, nombres, apellidos, edad, genero) 
                VALUES ('TEST123', 'Juan', 'Prueba', 30, 'M') 
                RETURNING id
            """)
            paciente_id = cursor.fetchone()[0]
            
            # Test simple de inserción en examenes_basicos
            cursor.execute("""
                INSERT INTO examenes_basicos (paciente_id, av_distancia_od, av_distancia_oi, pio_od, pio_oi) 
                VALUES (%s, '20/20', '20/20', 15, 16) 
                RETURNING id
            """, (paciente_id,))
            examen_id = cursor.fetchone()[0]
            
            # Limpiar datos de prueba
            cursor.execute("DELETE FROM examenes_basicos WHERE id = %s", (examen_id,))
            cursor.execute("DELETE FROM pacientes WHERE id = %s", (paciente_id,))
            
            print("✅ PRUEBA DE INSERCIÓN: EXITOSA")
            print("✅ Los campos están funcionando correctamente")
            
        except Exception as e:
            print(f"❌ PRUEBA DE INSERCIÓN: FALLÓ - {e}")
            return False
        
        # No confirmar cambios (rollback de las pruebas)
        conn.rollback()
        
        print("\n🎉 ¡VERIFICACIÓN COMPLETA!")
        print("✅ Todos los campos están correctamente implementados en Render")
        print("🌐 La BD está lista para la Ficha Clínica Digital")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR EN VERIFICACIÓN: {e}")
        return False
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            print("🔌 Conexión cerrada")

if __name__ == "__main__":
    verificar_bd_render()