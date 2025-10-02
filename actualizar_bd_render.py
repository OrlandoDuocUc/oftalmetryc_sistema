#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ACTUALIZAR BD RENDER - Ficha Clínica Digital
Conecta directamente a Render y agrega los campos faltantes
"""

import psycopg2
import sys

# Datos de conexión a Render
DATABASE_URL = "postgresql://oftalmetryc_user:0WdPbRIzVrbH6xYFCye20Q7ST4e3v7Kn@dpg-d3efatffte5s73chd9r0-a.oregon-postgres.render.com:5432/oftalmetryc_db"

def actualizar_bd_render():
    """Actualizar base de datos en Render con campos de ficha clínica"""
    print("🚀 CONECTANDO A RENDER DATABASE...")
    print("🗄️ BD: oftalmetryc_db (oftalmetryc_database)")
    print("=" * 60)
    
    try:
        # Conectar a Render
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("✅ Conexión exitosa a Render")
        print()
        
        # 1. EXPANDIR TABLA PACIENTES
        print("📋 EXPANDIENDO TABLA PACIENTES...")
        campos_pacientes = [
            "ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS ci VARCHAR(20);",
            "ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS nombres VARCHAR(100);",
            "ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS apellidos VARCHAR(100);",
            "ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS edad INTEGER;",
            "ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS genero VARCHAR(20);",
            "ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS hobby TEXT;"
        ]
        
        for sql in campos_pacientes:
            cursor.execute(sql)
            print(f"  ✅ {sql.split('ADD COLUMN IF NOT EXISTS')[1].split()[0]}")
        
        print()
        
        # 2. EXPANDIR TABLA EXAMENES_BASICOS
        print("👁️ EXPANDIENDO TABLA EXAMENES_BASICOS...")
        campos_examenes = [
            # Agudeza Visual
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS av_distancia_od VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS av_distancia_oi VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS av_distancia_ao VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS av_proximidad_od VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS av_proximidad_oi VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS av_proximidad_ao VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS pin_hole_od VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS pin_hole_oi VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS dominancia_ocular VARCHAR(10);",
            
            # Autorefractor
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS autorefractor_od_esfera VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS autorefractor_od_cilindro VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS autorefractor_od_eje VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS autorefractor_oi_esfera VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS autorefractor_oi_cilindro VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS autorefractor_oi_eje VARCHAR(10);",
            
            # RX Final
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_final_od_esfera VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_final_od_cilindro VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_final_od_eje VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_final_od_adicion VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_final_oi_esfera VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_final_oi_cilindro VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_final_oi_eje VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_final_oi_adicion VARCHAR(10);",
            
            # Lentes de Contacto
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lc_od_poder VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lc_od_curva_base VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lc_od_diametro VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lc_od_material VARCHAR(50);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lc_oi_poder VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lc_oi_curva_base VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lc_oi_diametro VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lc_oi_material VARCHAR(50);",
            
            # Presión Intraocular
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS pio_od INTEGER;",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS pio_oi INTEGER;",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS pio_metodo VARCHAR(50);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS pio_hora TIME;",
            
            # Tests Especializados
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS test_ishihara VARCHAR(50);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS test_hirschberg VARCHAR(50);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS cover_test VARCHAR(50);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS luces_worth VARCHAR(50);",
            
            # Lensometría
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lensometria_od_esfera VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lensometria_od_cilindro VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lensometria_od_eje VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lensometria_oi_esfera VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lensometria_oi_cilindro VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lensometria_oi_eje VARCHAR(10);",
            
            # Biomicroscopía
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS biomicroscopia_od TEXT;",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS biomicroscopia_oi TEXT;",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS biomicroscopia_conjuntiva VARCHAR(100);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS biomicroscopia_cornea VARCHAR(100);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS biomicroscopia_iris VARCHAR(100);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS biomicroscopia_pupila VARCHAR(100);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS biomicroscopia_cristalino VARCHAR(100);",
            
            # Subjetivo
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS subjetivo_od_esfera VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS subjetivo_od_cilindro VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS subjetivo_od_eje VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS subjetivo_oi_esfera VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS subjetivo_oi_cilindro VARCHAR(10);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS subjetivo_oi_eje VARCHAR(10);",
            
            # Oftalmoscopía
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS oftalmoscopia_od TEXT;",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS oftalmoscopia_oi TEXT;",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS oftalmoscopia_retina VARCHAR(100);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS oftalmoscopia_papila VARCHAR(100);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS oftalmoscopia_macula VARCHAR(100);",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS oftalmoscopia_vasos VARCHAR(100);",
            
            # Motilidad Ocular
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS motilidad_ducciones TEXT;",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS motilidad_versiones TEXT;",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS motilidad_convergencia VARCHAR(50);",
            
            # Campos adicionales
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS observaciones TEXT;",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS diagnostico TEXT;",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS recomendaciones TEXT;",
            "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS fecha_examen TIMESTAMP DEFAULT NOW();"
        ]
        
        for i, sql in enumerate(campos_examenes, 1):
            cursor.execute(sql)
            campo_nombre = sql.split('ADD COLUMN IF NOT EXISTS')[1].split()[0]
            print(f"  ✅ {i:2d}/72 - {campo_nombre}")
        
        print()
        
        # 3. EXPANDIR TABLA CONSULTAS_MEDICAS  
        print("🏥 EXPANDIENDO TABLA CONSULTAS_MEDICAS...")
        campos_consultas = [
            "ALTER TABLE consultas_medicas ADD COLUMN IF NOT EXISTS motivo_consulta TEXT;",
            "ALTER TABLE consultas_medicas ADD COLUMN IF NOT EXISTS diagnostico TEXT;",
            "ALTER TABLE consultas_medicas ADD COLUMN IF NOT EXISTS observaciones TEXT;",
            "ALTER TABLE consultas_medicas ADD COLUMN IF NOT EXISTS estado VARCHAR(50) DEFAULT 'Pendiente';",
            "ALTER TABLE consultas_medicas ADD COLUMN IF NOT EXISTS fecha_seguimiento DATE;",
            "ALTER TABLE consultas_medicas ADD COLUMN IF NOT EXISTS tratamiento TEXT;"
        ]
        
        for sql in campos_consultas:
            cursor.execute(sql)
            campo_nombre = sql.split('ADD COLUMN IF NOT EXISTS')[1].split()[0]
            print(f"  ✅ {campo_nombre}")
        
        # Confirmar cambios
        conn.commit()
        print()
        
        # 4. VERIFICAR RESULTADOS
        print("🔍 VERIFICANDO RESULTADOS...")
        
        # Contar campos en pacientes
        cursor.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'pacientes'")
        total_pacientes = cursor.fetchone()[0]
        
        # Contar campos en examenes_basicos
        cursor.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'examenes_basicos'")
        total_examenes = cursor.fetchone()[0]
        
        # Contar campos en consultas_medicas
        cursor.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'consultas_medicas'")
        total_consultas = cursor.fetchone()[0]
        
        print(f"✅ PACIENTES: {total_pacientes} campos totales")
        print(f"✅ EXAMENES_BASICOS: {total_examenes} campos totales")
        print(f"✅ CONSULTAS_MEDICAS: {total_consultas} campos totales")
        print()
        
        print("🎉 ¡BD DE RENDER ACTUALIZADA EXITOSAMENTE!")
        print("🌐 La Ficha Clínica Digital ya está lista en producción")
        print("🔗 Disponible en: https://oftalmetryc-sistema.onrender.com/ficha-clinica")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("🔧 Verifica la conexión a internet y los datos de BD")
        return False
        
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            print("🔌 Conexión cerrada")
    
    return True

if __name__ == "__main__":
    print("🔧 ACTUALIZADOR BD RENDER - FICHA CLÍNICA DIGITAL")
    print("=" * 60)
    actualizar_bd_render()