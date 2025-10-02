#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRUEBA COMPLETA - Flujo Paciente + Ficha Clínica
Demuestra el proceso completo desde creación hasta examen
"""

import psycopg2
import sys
from datetime import datetime

# Datos de conexión a Render
DATABASE_URL = "postgresql://oftalmetryc_user:0WdPbRIzVrbH6xYFCye20Q7ST4e3v7Kn@dpg-d3efatffte5s73chd9r0-a.oregon-postgres.render.com:5432/oftalmetryc_db"

def demostrar_flujo_completo():
    """Demostrar el flujo completo del sistema"""
    print("🚀 DEMOSTRACIÓN DEL FLUJO COMPLETO")
    print("📋 Creación de Paciente + Ficha Clínica Digital")
    print("=" * 60)
    
    try:
        # Conectar a Render
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("✅ Conexión exitosa a Render")
        print()
        
        # PASO 1: CREAR PACIENTE DE PRUEBA
        print("👤 PASO 1: CREAR PACIENTE DE PRUEBA")
        print("-" * 40)
        
        paciente_data = {
            'ci': '1234567890',
            'rut': '12345678',
            'nombres': 'Juan Carlos',
            'apellidos': 'Pérez González',
            'nombre': 'Juan Carlos',
            'apellido': 'Pérez González',
            'edad': 35,
            'genero': 'M',
            'telefono': '0987654321',
            'email': 'juan.perez@email.com',
            'direccion': 'Av. Principal 123, Quito',
            'fecha_nacimiento': '1988-05-15',
            'ocupacion': 'Ingeniero',
            'contacto_emergencia': 'María Pérez',
            'telefono_emergencia': '0987654322',
            'observaciones': 'Paciente con antecedentes de miopía',
            'estado': 'Activo'
        }
        
        # Verificar si el paciente ya existe
        cursor.execute("SELECT id FROM pacientes WHERE ci = %s", (paciente_data['ci'],))
        existing = cursor.fetchone()
        
        if existing:
            paciente_id = existing[0]
            print(f"✅ Paciente ya existe con ID: {paciente_id}")
        else:
            # Insertar nuevo paciente
            insert_query = """
                INSERT INTO pacientes (
                    ci, rut, nombres, apellidos, nombre, apellido, edad, genero,
                    telefono, email, direccion, fecha_nacimiento, ocupacion,
                    contacto_emergencia, telefono_emergencia, observaciones, estado,
                    created_at, updated_at
                ) VALUES (
                    %(ci)s, %(rut)s, %(nombres)s, %(apellidos)s, %(nombre)s, %(apellido)s,
                    %(edad)s, %(genero)s, %(telefono)s, %(email)s, %(direccion)s,
                    %(fecha_nacimiento)s, %(ocupacion)s, %(contacto_emergencia)s,
                    %(telefono_emergencia)s, %(observaciones)s, %(estado)s,
                    NOW(), NOW()
                ) RETURNING id
            """
            
            cursor.execute(insert_query, paciente_data)
            paciente_id = cursor.fetchone()[0]
            print(f"✅ Paciente creado exitosamente con ID: {paciente_id}")
        
        print(f"📋 CI: {paciente_data['ci']}")
        print(f"📋 Nombre: {paciente_data['nombres']} {paciente_data['apellidos']}")
        print(f"📋 Edad: {paciente_data['edad']} años")
        print()
        
        # PASO 2: SIMULAR BÚSQUEDA EN FICHA CLÍNICA
        print("🔍 PASO 2: BUSCAR PACIENTE EN FICHA CLÍNICA")
        print("-" * 45)
        
        # Búsqueda por CI (simula el formulario de ficha clínica)
        cursor.execute("""
            SELECT id, ci, nombres, apellidos, edad, genero, telefono, email
            FROM pacientes 
            WHERE ci = %s AND estado = 'Activo'
        """, (paciente_data['ci'],))
        
        paciente_encontrado = cursor.fetchone()
        
        if paciente_encontrado:
            print(f"✅ PACIENTE ENCONTRADO:")
            print(f"   ID: {paciente_encontrado[0]}")
            print(f"   CI: {paciente_encontrado[1]}")
            print(f"   Nombre: {paciente_encontrado[2]} {paciente_encontrado[3]}")
            print(f"   Edad: {paciente_encontrado[4]} años")
            print(f"   Género: {paciente_encontrado[5]}")
            print(f"   Teléfono: {paciente_encontrado[6]}")
            print()
        else:
            print("❌ Paciente no encontrado")
            return
        
        # PASO 3: CREAR CONSULTA MÉDICA PRIMERO
        print("🏥 PASO 3: CREAR CONSULTA MÉDICA")
        print("-" * 35)
        
        consulta_data = {
            'paciente_id': paciente_id,
            'fecha_consulta': datetime.now(),
            'motivo_consulta': 'Control oftalmológico de rutina',
            'diagnostico': 'Hipermetropía con astigmatismo bilateral, presbicia incipiente',
            'observaciones': 'Paciente colaborador, buen estado general',
            'estado': 'Completada',
            'tratamiento': 'Prescripción de lentes bifocales',
            'proxima_cita': '2026-01-15'
        }
        
        insert_consulta = """
            INSERT INTO consultas_medicas (
                paciente_id, fecha_consulta, motivo_consulta, diagnostico,
                observaciones, estado, tratamiento, proxima_cita,
                created_at, updated_at
            ) VALUES (
                %(paciente_id)s, %(fecha_consulta)s, %(motivo_consulta)s, %(diagnostico)s,
                %(observaciones)s, %(estado)s, %(tratamiento)s, %(proxima_cita)s,
                NOW(), NOW()
            ) RETURNING id
        """
        
        cursor.execute(insert_consulta, consulta_data)
        consulta_id = cursor.fetchone()[0]
        
        print(f"✅ Consulta médica creada con ID: {consulta_id}")
        print(f"📋 Motivo: {consulta_data['motivo_consulta']}")
        print(f"💊 Tratamiento: {consulta_data['tratamiento']}")
        print(f"📅 Próxima cita: {consulta_data['proxima_cita']}")
        print()
        
        # PASO 4: CREAR FICHA CLÍNICA CON LA CONSULTA
        print("👁️ PASO 4: CREAR FICHA CLÍNICA DIGITAL")
        print("-" * 42)
        
        # Datos de examen oftalmológico completo
        examen_data = {
            'consulta_id': consulta_id,  # Ahora usamos el ID de la consulta creada
            'fecha_examen': datetime.now(),
            
            # Agudeza Visual
            'av_distancia_od': '20/20',
            'av_distancia_oi': '20/25',
            'av_distancia_ao': '20/20',
            'av_proximidad_od': 'J1',
            'av_proximidad_oi': 'J2',
            'av_proximidad_ao': 'J1',
            'pin_hole_od': '20/20',
            'pin_hole_oi': '20/20',
            'dominancia_ocular': 'OD',
            
            # Autorefractor
            'autorefractor_od_esfera': '+1.50',
            'autorefractor_od_cilindro': '-0.75',
            'autorefractor_od_eje': '180',
            'autorefractor_oi_esfera': '+1.25',
            'autorefractor_oi_cilindro': '-0.50',
            'autorefractor_oi_eje': '175',
            
            # RX Final
            'rx_final_od_esfera': '+1.75',
            'rx_final_od_cilindro': '-0.75',
            'rx_final_od_eje': '180',
            'rx_final_od_adicion': '+2.00',
            'rx_final_oi_esfera': '+1.50',
            'rx_final_oi_cilindro': '-0.50',
            'rx_final_oi_eje': '175',
            'rx_final_oi_adicion': '+2.00',
            
            # Presión Intraocular
            'pio_od': 15,
            'pio_oi': 16,
            'pio_metodo': 'Goldmann',
            'pio_hora': '10:30:00',
            
            # Tests Especializados
            'test_ishihara': 'Normal',
            'test_hirschberg': 'Centrado',
            'cover_test': 'Sin desviación',
            'luces_worth': 'Fusión normal',
            
            # Lensometría
            'lensometria_od_esfera': '+1.50',
            'lensometria_od_cilindro': '-0.75',
            'lensometria_od_eje': '180',
            'lensometria_oi_esfera': '+1.25',
            'lensometria_oi_cilindro': '-0.50',
            'lensometria_oi_eje': '175',
            
            # Biomicroscopía
            'biomicroscopia_od': 'Estructuras anteriores normales',
            'biomicroscopia_oi': 'Estructuras anteriores normales',
            'biomicroscopia_conjuntiva': 'Sin hiperemia',
            'biomicroscopia_cornea': 'Transparente',
            'biomicroscopia_iris': 'Patrón normal',
            'biomicroscopia_pupila': 'Reactiva',
            'biomicroscopia_cristalino': 'Transparente',
            
            # Examen Subjetivo
            'subjetivo_od_esfera': '+1.75',
            'subjetivo_od_cilindro': '-0.75',
            'subjetivo_od_eje': '180',
            'subjetivo_oi_esfera': '+1.50',
            'subjetivo_oi_cilindro': '-0.50',
            'subjetivo_oi_eje': '175',
            
            # Oftalmoscopía
            'oftalmoscopia_od': 'Fondo normal',
            'oftalmoscopia_oi': 'Fondo normal',
            'oftalmoscopia_retina': 'Sin alteraciones',
            'oftalmoscopia_papila': 'Bien delimitada',
            'oftalmoscopia_macula': 'Reflejo foveal presente',
            'oftalmoscopia_vasos': 'Calibre normal',
            
            # Motilidad
            'motilidad_ducciones': 'Completas en todas direcciones',
            'motilidad_versiones': 'Coordinadas',
            'motilidad_convergencia': 'Normal',
            
            # Observaciones
            'observaciones': 'Examen oftalmológico completo sin hallazgos patológicos significativos',
            'diagnostico': 'Hipermetropía con astigmatismo bilateral, presbicia incipiente',
            'recomendaciones': 'Lentes bifocales, control anual'
        }
        
        # Insertar examen básico
        insert_examen = """
            INSERT INTO examenes_basicos (
                consulta_id, fecha_examen,
                av_distancia_od, av_distancia_oi, av_distancia_ao,
                av_proximidad_od, av_proximidad_oi, av_proximidad_ao,
                pin_hole_od, pin_hole_oi, dominancia_ocular,
                autorefractor_od_esfera, autorefractor_od_cilindro, autorefractor_od_eje,
                autorefractor_oi_esfera, autorefractor_oi_cilindro, autorefractor_oi_eje,
                rx_final_od_esfera, rx_final_od_cilindro, rx_final_od_eje, rx_final_od_adicion,
                rx_final_oi_esfera, rx_final_oi_cilindro, rx_final_oi_eje, rx_final_oi_adicion,
                pio_od, pio_oi, pio_metodo, pio_hora,
                test_ishihara, test_hirschberg, cover_test, luces_worth,
                lensometria_od_esfera, lensometria_od_cilindro, lensometria_od_eje,
                lensometria_oi_esfera, lensometria_oi_cilindro, lensometria_oi_eje,
                biomicroscopia_od, biomicroscopia_oi, biomicroscopia_conjuntiva,
                biomicroscopia_cornea, biomicroscopia_iris, biomicroscopia_pupila, biomicroscopia_cristalino,
                subjetivo_od_esfera, subjetivo_od_cilindro, subjetivo_od_eje,
                subjetivo_oi_esfera, subjetivo_oi_cilindro, subjetivo_oi_eje,
                oftalmoscopia_od, oftalmoscopia_oi, oftalmoscopia_retina,
                oftalmoscopia_papila, oftalmoscopia_macula, oftalmoscopia_vasos,
                motilidad_ducciones, motilidad_versiones, motilidad_convergencia,
                observaciones, diagnostico, recomendaciones
            ) VALUES (
                %(consulta_id)s, %(fecha_examen)s,
                %(av_distancia_od)s, %(av_distancia_oi)s, %(av_distancia_ao)s,
                %(av_proximidad_od)s, %(av_proximidad_oi)s, %(av_proximidad_ao)s,
                %(pin_hole_od)s, %(pin_hole_oi)s, %(dominancia_ocular)s,
                %(autorefractor_od_esfera)s, %(autorefractor_od_cilindro)s, %(autorefractor_od_eje)s,
                %(autorefractor_oi_esfera)s, %(autorefractor_oi_cilindro)s, %(autorefractor_oi_eje)s,
                %(rx_final_od_esfera)s, %(rx_final_od_cilindro)s, %(rx_final_od_eje)s, %(rx_final_od_adicion)s,
                %(rx_final_oi_esfera)s, %(rx_final_oi_cilindro)s, %(rx_final_oi_eje)s, %(rx_final_oi_adicion)s,
                %(pio_od)s, %(pio_oi)s, %(pio_metodo)s, %(pio_hora)s,
                %(test_ishihara)s, %(test_hirschberg)s, %(cover_test)s, %(luces_worth)s,
                %(lensometria_od_esfera)s, %(lensometria_od_cilindro)s, %(lensometria_od_eje)s,
                %(lensometria_oi_esfera)s, %(lensometria_oi_cilindro)s, %(lensometria_oi_eje)s,
                %(biomicroscopia_od)s, %(biomicroscopia_oi)s, %(biomicroscopia_conjuntiva)s,
                %(biomicroscopia_cornea)s, %(biomicroscopia_iris)s, %(biomicroscopia_pupila)s, %(biomicroscopia_cristalino)s,
                %(subjetivo_od_esfera)s, %(subjetivo_od_cilindro)s, %(subjetivo_od_eje)s,
                %(subjetivo_oi_esfera)s, %(subjetivo_oi_cilindro)s, %(subjetivo_oi_eje)s,
                %(oftalmoscopia_od)s, %(oftalmoscopia_oi)s, %(oftalmoscopia_retina)s,
                %(oftalmoscopia_papila)s, %(oftalmoscopia_macula)s, %(oftalmoscopia_vasos)s,
                %(motilidad_ducciones)s, %(motilidad_versiones)s, %(motilidad_convergencia)s,
                %(observaciones)s, %(diagnostico)s, %(recomendaciones)s
            ) RETURNING id
        """
        
        cursor.execute(insert_examen, examen_data)
        examen_id = cursor.fetchone()[0]
        
        print(f"✅ Ficha clínica creada con ID: {examen_id}")
        print(f"👁️ Agudeza Visual OD: {examen_data['av_distancia_od']}")
        print(f"👁️ Agudeza Visual OI: {examen_data['av_distancia_oi']}")
        print(f"📊 PIO OD: {examen_data['pio_od']} mmHg")
        print(f"📊 PIO OI: {examen_data['pio_oi']} mmHg")
        print(f"🔬 Diagnóstico: {examen_data['diagnostico']}")
        print()
        
        # Confirmar todos los cambios
        conn.commit()
        
        # RESUMEN FINAL
        print("🎉 FLUJO COMPLETADO EXITOSAMENTE")
        print("=" * 50)
        print(f"✅ Paciente ID: {paciente_id}")
        print(f"✅ Consulta ID: {consulta_id}")
        print(f"✅ Examen ID: {examen_id}")
        print()
        print("🌐 ACCESOS DIRECTOS:")
        print("📋 Crear Paciente: https://oftalmetryc-sistema.onrender.com/pacientes/nuevo")
        print("🔍 Ver Pacientes: https://oftalmetryc-sistema.onrender.com/pacientes")
        print("👁️ Ficha Clínica: https://oftalmetryc-sistema.onrender.com/ficha-clinica")
        print()
        print("💡 FLUJO DE USO:")
        print("1. Crear paciente en /pacientes/nuevo")
        print("2. Buscar paciente en /ficha-clinica por CI")
        print("3. Completar examen oftalmológico")
        print("4. Guardar y generar reporte")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            print("🔌 Conexión cerrada")

if __name__ == "__main__":
    demostrar_flujo_completo()