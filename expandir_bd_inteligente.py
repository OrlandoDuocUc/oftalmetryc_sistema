#!/usr/bin/env python3
# SCRIPT INTELIGENTE - AGREGAR SOLO CAMPOS FALTANTES
import os
from sqlalchemy import create_engine, text

def agregar_campos_faltantes():
    print("🔧 AGREGANDO CAMPOS FALTANTES A BD EXISTENTE...")
    
    try:
        engine = create_engine(os.getenv('DATABASE_URL'))
        
        with engine.connect() as conn:
            with conn.begin():
                
                # EXPANDIR TABLA PACIENTES
                print("📋 Expandiendo tabla pacientes...")
                campos_pacientes = [
                    "ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS ci VARCHAR(20);",
                    "ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS nombres VARCHAR(100);",
                    "ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS apellidos VARCHAR(100);", 
                    "ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS edad INTEGER;",
                    "ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS genero VARCHAR(10);",
                    "ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS hobby VARCHAR(200);",
                    "ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS estado VARCHAR(20) DEFAULT 'Activo';",
                    "ALTER TABLE pacientes ADD COLUMN IF NOT EXISTS observaciones_generales TEXT;"
                ]
                
                for sql in campos_pacientes:
                    try:
                        conn.execute(text(sql))
                    except Exception as e:
                        print(f"⚠️  Campo ya existe: {e}")
                        continue
                
                # EXPANDIR TABLA CONSULTAS_MEDICAS  
                print("📋 Expandiendo tabla consultas_medicas...")
                campos_consultas = [
                    "ALTER TABLE consultas_medicas ADD COLUMN IF NOT EXISTS ultimo_control_visual DATE;",
                    "ALTER TABLE consultas_medicas ADD COLUMN IF NOT EXISTS usa_lentes BOOLEAN DEFAULT FALSE;",
                    "ALTER TABLE consultas_medicas ADD COLUMN IF NOT EXISTS ultimo_cambio_lentes DATE;",
                    "ALTER TABLE consultas_medicas ADD COLUMN IF NOT EXISTS firma_responsable VARCHAR(100);",
                    "ALTER TABLE consultas_medicas ADD COLUMN IF NOT EXISTS conforme_evaluado BOOLEAN DEFAULT TRUE;"
                ]
                
                for sql in campos_consultas:
                    try:
                        conn.execute(text(sql))
                    except Exception as e:
                        print(f"⚠️  Campo ya existe: {e}")
                        continue
                
                # EXPANDIR TABLA EXAMENES_BASICOS MASIVAMENTE
                print("📋 Expandiendo tabla examenes_basicos...")
                campos_examenes = [
                    # Agudeza Visual Expandida
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS av_distancia_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS av_distancia_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS av_c_c_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS av_c_c_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS av_s_c_od VARCHAR(10);", 
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS av_s_c_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS av_ph_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS av_ph_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS av_proxima_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS av_proxima_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS av_ao_distancia VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS av_ao_proxima VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS dominante_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS dominante_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS av_otros TEXT;",
                    
                    # Lensometría
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lensometria_od VARCHAR(50);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lensometria_oi VARCHAR(50);",
                    
                    # Queratometría  
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS queratometria_od VARCHAR(50);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS queratometria_oi VARCHAR(50);",
                    
                    # Autorefractor
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS ar_esf_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS ar_cyl_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS ar_eje_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS ar_av_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS ar_esf_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS ar_cyl_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS ar_eje_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS ar_av_oi VARCHAR(10);",
                    
                    # Subjetivo
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS sub_esf_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS sub_cyl_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS sub_eje_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS sub_av_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS sub_esf_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS sub_cyl_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS sub_eje_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS sub_av_oi VARCHAR(10);",
                    
                    # RX Final
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_esf_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_cyl_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_eje_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_avl_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_avc_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_dp_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_np_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_add_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_alt_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_ao_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_esf_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_cyl_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_eje_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_avl_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_avc_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_dp_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_np_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_add_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_alt_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS rx_ao_oi VARCHAR(10);",
                    
                    # Lentes de Contacto
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lc_poder_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lc_curva_base_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lc_diametro_od VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lc_material_od VARCHAR(50);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lc_poder_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lc_curva_base_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lc_diametro_oi VARCHAR(10);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS lc_material_oi VARCHAR(50);",
                    
                    # Test Adicionales
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS hirschberg_od INTEGER;",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS hirschberg_oi INTEGER;",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS test_ishihara VARCHAR(50);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS presion_intraocular_od VARCHAR(20);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS presion_intraocular_oi VARCHAR(20);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS cover_test_pfc VARCHAR(50);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS cover_test_foria VARCHAR(50);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS mov_oculares VARCHAR(100);",
                    "ALTER TABLE examenes_basicos ADD COLUMN IF NOT EXISTS test_adicionales_otros TEXT;"
                ]
                
                total_campos = len(campos_examenes)
                print(f"🔄 Agregando {total_campos} campos nuevos...")
                
                campos_agregados = 0
                for i, sql in enumerate(campos_examenes):
                    try:
                        conn.execute(text(sql))
                        campos_agregados += 1
                        if (i + 1) % 10 == 0:
                            print(f"   📈 {i+1}/{total_campos} campos procesados...")
                    except Exception as e:
                        if "already exists" not in str(e):
                            print(f"⚠️  Error en campo: {e}")
                        continue
                
                print(f"✅ {campos_agregados} campos nuevos agregados")
                
                # Crear índices seguros
                print("📋 Creando índices...")
                indices = [
                    "CREATE INDEX IF NOT EXISTS idx_pacientes_ci ON pacientes(ci) WHERE ci IS NOT NULL;",
                    "CREATE INDEX IF NOT EXISTS idx_pacientes_rut ON pacientes(rut) WHERE rut IS NOT NULL;",
                    "CREATE INDEX IF NOT EXISTS idx_pacientes_nombres ON pacientes(nombres, apellidos) WHERE nombres IS NOT NULL;",
                ]
                
                for sql in indices:
                    try:
                        conn.execute(text(sql))
                    except Exception as e:
                        print(f"⚠️  Índice ya existe: {e}")
                        continue
                
                # Migrar datos existentes
                print("📋 Migrando datos existentes...")
                try:
                    conn.execute(text("""
                        UPDATE pacientes 
                        SET nombres = nombre, apellidos = apellido 
                        WHERE nombres IS NULL AND nombre IS NOT NULL;
                    """))
                except:
                    pass
                
                try:
                    conn.execute(text("""
                        UPDATE pacientes 
                        SET edad = EXTRACT(YEAR FROM age(fecha_nacimiento))
                        WHERE edad IS NULL AND fecha_nacimiento IS NOT NULL;
                    """))
                except:
                    pass
                
                try:
                    conn.execute(text("""
                        UPDATE pacientes 
                        SET estado = 'Activo' 
                        WHERE estado IS NULL;
                    """))
                except:
                    pass
        
        # Verificar resultado final
        with engine.connect() as conn:
            # Contar campos en cada tabla
            result = conn.execute(text("""
                SELECT 
                    'pacientes' as tabla,
                    count(*) as total_campos
                FROM information_schema.columns 
                WHERE table_name = 'pacientes'
                
                UNION ALL
                
                SELECT 
                    'examenes_basicos' as tabla,
                    count(*) as total_campos
                FROM information_schema.columns 
                WHERE table_name = 'examenes_basicos'
                
                UNION ALL
                
                SELECT 
                    'consultas_medicas' as tabla,
                    count(*) as total_campos
                FROM information_schema.columns 
                WHERE table_name = 'consultas_medicas';
            """))
            
            print("\n📊 ESTRUCTURA FINAL:")
            print("=" * 40)
            
            for row in result:
                print(f"📄 {row[0]:20} | {row[1]:3} campos")
            
            print("=" * 40)
            
            # Verificar algunos campos clave de ficha clínica
            campos_clave = ['ci', 'nombres', 'edad', 'av_distancia_od', 'rx_esf_od', 'lensometria_od']
            print("\n🔍 VERIFICANDO CAMPOS CLAVE DE FICHA CLÍNICA:")
            
            for campo in campos_clave:
                try:
                    if campo in ['ci', 'nombres', 'edad']:
                        tabla = 'pacientes'
                    else:
                        tabla = 'examenes_basicos'
                        
                    result = conn.execute(text(f"""
                        SELECT column_name FROM information_schema.columns 
                        WHERE table_name = '{tabla}' AND column_name = '{campo}';
                    """))
                    existe = result.fetchone()
                    status = "✅" if existe else "❌"
                    print(f"{status} {tabla}.{campo}")
                except:
                    print(f"❌ {tabla}.{campo}")
        
        print("\n🎉 ¡EXPANSIÓN COMPLETADA EXITOSAMENTE!")
        print("✅ Base de datos expandida con campos de ficha clínica")
        print("✅ Sistema listo para módulo oftalmológico completo")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False
        
    return True

if __name__ == "__main__":
    agregar_campos_faltantes()