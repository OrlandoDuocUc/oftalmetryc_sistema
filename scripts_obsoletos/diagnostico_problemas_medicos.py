#!/usr/bin/env python3
"""
DIAGNÓSTICO DE PROBLEMAS DEL SISTEMA MÉDICO
==========================================

Este script diagnostica los problemas reportados:
1. Pacientes no aparecen en búsqueda
2. Rutas duplicadas confusas
3. Ficha clínica no visible en todas las pantallas

Verifica BD y rutas del sistema.
"""

import os
import sys
import psycopg2
from pathlib import Path

def verificar_pacientes_bd():
    """Verifica pacientes en base de datos de Render"""
    
    print("🔍 DIAGNÓSTICO: PROBLEMAS DEL SISTEMA MÉDICO")
    print("=" * 50)
    
    # Configuración de BD Render
    DATABASE_URL = "postgresql://oftalmetryc_user:1t9ypAEbUrZlL0k0JHyAqiiwpCuGUgmt@dpg-cs67qm3tq21c73fnqkg0-a.oregon-postgres.render.com/oftalmetryc_db"
    
    try:
        print("\n📊 VERIFICANDO BASE DE DATOS:")
        print("-" * 35)
        
        # Conectar a BD
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Verificar tabla pacientes
        cursor.execute("SELECT COUNT(*) FROM pacientes;")
        total_pacientes = cursor.fetchone()[0]
        print(f"👥 Total pacientes registrados: {total_pacientes}")
        
        # Verificar últimos pacientes
        cursor.execute("""
            SELECT id, rut, ci, nombre, apellido, created_at 
            FROM pacientes 
            ORDER BY created_at DESC 
            LIMIT 5;
        """)
        
        ultimos_pacientes = cursor.fetchall()
        
        print(f"\n📋 ÚLTIMOS 5 PACIENTES REGISTRADOS:")
        print("-" * 40)
        for paciente in ultimos_pacientes:
            id_pac, rut, ci, nombre, apellido, fecha = paciente
            print(f"🏷️ ID: {id_pac} | RUT: {rut} | CI: {ci}")
            print(f"👤 Nombre: {nombre} {apellido}")
            print(f"📅 Registrado: {fecha}")
            print("-" * 30)
        
        # Verificar tabla examenes_basicos
        cursor.execute("SELECT COUNT(*) FROM examenes_basicos;")
        total_examenes = cursor.fetchone()[0]
        print(f"\n🔬 Total exámenes/fichas clínicas: {total_examenes}")
        
        # Verificar consultas médicas
        try:
            cursor.execute("SELECT COUNT(*) FROM consultas_medicas;")
            total_consultas = cursor.fetchone()[0]
            print(f"📋 Total consultas médicas: {total_consultas}")
        except:
            print("⚠️ Tabla consultas_medicas no existe")
        
        cursor.close()
        conn.close()
        
        print(f"\n✅ CONEXIÓN A BD: Exitosa")
        
    except Exception as e:
        print(f"❌ ERROR BD: {str(e)}")
    
    return True

def analizar_rutas_duplicadas():
    """Analiza rutas duplicadas confusas"""
    
    print(f"\n🔀 ANÁLISIS: RUTAS DUPLICADAS CONFUSAS")
    print("-" * 45)
    
    rutas_confusas = {
        "CREAR FICHA CLÍNICA": [
            "/ficha-clinica",
            "/consultas/nueva"
        ],
        "VER CONSULTAS": [
            "/consultas", 
            "/historial-consultas"
        ]
    }
    
    for funcionalidad, rutas in rutas_confusas.items():
        print(f"\n🎯 {funcionalidad}:")
        for i, ruta in enumerate(rutas, 1):
            print(f"   {i}. {ruta}")
        print(f"   ⚠️ PROBLEMA: {len(rutas)} rutas para la misma función")
    
    print(f"\n💡 RECOMENDACIÓN:")
    print("   • Unificar en UNA SOLA ruta por funcionalidad")
    print("   • Eliminar rutas duplicadas")
    print("   • Redireccionar rutas obsoletas")

def verificar_navegacion_faltante():
    """Verifica qué plantillas NO tienen 'Ficha Clínica'"""
    
    print(f"\n🧭 ANÁLISIS: NAVEGACIÓN FALTANTE")
    print("-" * 40)
    
    templates_dir = Path(r"c:\Users\Usuario\Desktop\MAURICIO TODO\TRABAJO MAURICIO UDLA\VERSION FINAL PRO ALMONACID\version 2 optica almonacid (FINAL) BUENA\optica-maipu\adapters\input\flask_app\templates\medical")
    
    archivos_medicos = [
        "dashboard_medico.html",
        "pacientes.html",
        "consultas.html", 
        "ficha_clinica.html",
        "nuevo_paciente.html",
        "nueva_consulta.html",
        "detalle_paciente.html",
        "detalle_consulta.html",
        "examen_oftalmologico.html"
    ]
    
    problemas_navegacion = []
    
    for archivo in archivos_medicos:
        archivo_path = templates_dir / archivo
        if archivo_path.exists():
            with open(archivo_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Verificar si tiene "ficha-clinica" en el menú
            if 'ficha-clinica' not in contenido:
                problemas_navegacion.append(archivo)
    
    print(f"📋 Archivos SIN 'Ficha Clínica' en menú:")
    for archivo in problemas_navegacion:
        print(f"   ❌ {archivo}")
    
    if not problemas_navegacion:
        print("   ✅ Todos los archivos tienen 'Ficha Clínica'")
    
    return problemas_navegacion

def generar_plan_solucion():
    """Genera plan de solución para todos los problemas"""
    
    print(f"\n🎯 PLAN DE SOLUCIÓN:")
    print("=" * 25)
    
    print(f"\n1️⃣ PROBLEMA PACIENTES NO APARECEN:")
    print("   🔧 Verificar modelo de BD usado en búsqueda")
    print("   🔧 Revisar encoding de caracteres especiales")
    print("   🔧 Confirmar commit de transacción BD")
    
    print(f"\n2️⃣ PROBLEMA RUTAS DUPLICADAS:")
    print("   🔧 Unificar '/ficha-clinica' como ruta principal")
    print("   🔧 Redirigir '/consultas/nueva' → '/ficha-clinica'")
    print("   🔧 Eliminar confusión en navegación")
    
    print(f"\n3️⃣ PROBLEMA NAVEGACIÓN FALTANTE:")
    print("   🔧 Agregar 'Ficha Clínica' a TODAS las plantillas")
    print("   🔧 Verificar que aparezca en dropdown médico")
    print("   🔧 Mantener consistencia visual")
    
    print(f"\n✨ RESULTADO ESPERADO:")
    print("   ✅ Pacientes aparecen en búsqueda")
    print("   ✅ Una sola ruta clara para ficha clínica")
    print("   ✅ 'Ficha Clínica' visible desde cualquier pantalla")

if __name__ == "__main__":
    verificar_pacientes_bd()
    analizar_rutas_duplicadas()
    navegacion_faltante = verificar_navegacion_faltante()
    generar_plan_solucion()