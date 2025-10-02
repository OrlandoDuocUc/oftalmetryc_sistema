#!/usr/bin/env python3
"""
VERIFICADOR COMPLETO DEL SISTEMA
Prueba todas las funcionalidades médicas
"""
import os
import psycopg2
from datetime import datetime
import requests
import json

class VerificadorCompleto:
    def __init__(self):
        self.DATABASE_URL = "postgresql://oftalmetryc_user:0WdPbRIzVrbH6xYFCye20Q7ST4e3v7Kn@dpg-d3efatffte5s73chd9r0-a.oregon-postgres.render.com/oftalmetryc_db"
        self.base_url = "http://127.0.0.1:5000"
    
    def verificar_bd(self):
        """Verificar conexión y estructura de la BD"""
        print("🔍 VERIFICANDO BASE DE DATOS")
        print("-" * 40)
        
        try:
            conn = psycopg2.connect(self.DATABASE_URL)
            cur = conn.cursor()
            
            # Verificar tablas
            cur.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;")
            tables = cur.fetchall()
            
            expected_tables = ['consulta_medica', 'paciente', 'usuario', 'rol', 'producto', 'sale', 'sale_detail', 'migrations']
            
            print(f"✅ Conexión exitosa")
            print(f"📊 Tablas encontradas: {len(tables)}")
            
            for table in tables:
                status = "✅" if table[0] in expected_tables else "❓"
                print(f"   {status} {table[0]}")
            
            # Verificar campos de consulta_medica
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'consulta_medica' 
                ORDER BY ordinal_position;
            """)
            campos = cur.fetchall()
            
            print(f"\n👁️ Campos en consulta_medica: {len(campos)}")
            campos_oftalmologicos = [
                'od_sin_correccion', 'oi_sin_correccion', 'od_esfera', 'oi_esfera',
                'pio_od', 'pio_oi', 'conjuntiva_od', 'conjuntiva_oi', 'papila_od', 'papila_oi'
            ]
            
            for campo in campos_oftalmologicos:
                existe = any(campo in str(c[0]) for c in campos)
                status = "✅" if existe else "❌"
                print(f"   {status} {campo}")
            
            # Verificar datos
            cur.execute("SELECT COUNT(*) FROM usuario;")
            usuarios = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM paciente;")
            pacientes = cur.fetchone()[0]
            
            cur.execute("SELECT COUNT(*) FROM consulta_medica;")
            consultas = cur.fetchone()[0]
            
            print(f"\n📊 DATOS:")
            print(f"   👥 Usuarios: {usuarios}")
            print(f"   🏥 Pacientes: {pacientes}")
            print(f"   👁️ Consultas: {consultas}")
            
            cur.close()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def crear_paciente_prueba(self):
        """Crear un paciente de prueba"""
        print("\n🏥 CREANDO PACIENTE DE PRUEBA")
        print("-" * 40)
        
        try:
            conn = psycopg2.connect(self.DATABASE_URL)
            cur = conn.cursor()
            
            # Insertar paciente
            cur.execute("""
                INSERT INTO paciente (rut, nombre, apellido, fecha_nacimiento, telefono, email, sexo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, ('12345678-9', 'Juan Carlos', 'Pérez López', '1985-03-15', '+56912345678', 'juan.perez@email.com', 'M'))
            
            paciente_id = cur.fetchone()[0]
            conn.commit()
            
            print(f"✅ Paciente creado con ID: {paciente_id}")
            
            cur.close()
            conn.close()
            
            return paciente_id
            
        except Exception as e:
            print(f"❌ Error creando paciente: {e}")
            return None
    
    def crear_consulta_prueba(self, paciente_id):
        """Crear una consulta médica completa"""
        print("\n👁️ CREANDO CONSULTA MÉDICA COMPLETA")
        print("-" * 40)
        
        try:
            conn = psycopg2.connect(self.DATABASE_URL)
            cur = conn.cursor()
            
            # Insertar consulta con todos los campos oftalmológicos
            cur.execute("""
                INSERT INTO consulta_medica (
                    paciente_id, medico_id, motivo_consulta, diagnostico, tratamiento,
                    antecedentes_familiares, antecedentes_personales,
                    od_sin_correccion, oi_sin_correccion, od_con_correccion, oi_con_correccion,
                    od_esfera, od_cilindro, od_eje, oi_esfera, oi_cilindro, oi_eje,
                    pio_od, pio_oi, metodo_tonometria,
                    conjuntiva_od, conjuntiva_oi, cornea_od, cornea_oi,
                    papila_od, papila_oi, macula_od, macula_oi,
                    plan_tratamiento, observaciones
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                ) RETURNING id;
            """, (
                paciente_id, 2, 'Control rutinario de miopía', 'Miopía bilateral estable', 'Continuar con lentes actuales',
                'Padre con glaucoma', 'Sin antecedentes relevantes',
                '20/40', '20/40', '20/20', '20/20',
                '-2.50', '-0.50', '180', '-2.75', '-0.25', '175',
                '14', '15', 'Goldmann',
                'Normal', 'Normal', 'Transparente', 'Transparente',
                'Normal, excavación 0.2', 'Normal, excavación 0.2', 'Normal', 'Normal',
                'Control en 6 meses', 'Paciente cumplidor del tratamiento'
            ))
            
            consulta_id = cur.fetchone()[0]
            conn.commit()
            
            print(f"✅ Consulta creada con ID: {consulta_id}")
            
            cur.close()
            conn.close()
            
            return consulta_id
            
        except Exception as e:
            print(f"❌ Error creando consulta: {e}")
            return None
    
    def verificar_consultas_api(self):
        """Verificar que las consultas aparecen en la API"""
        print("\n🔗 VERIFICANDO API DE CONSULTAS")
        print("-" * 40)
        
        try:
            # Verificar endpoint de consultas
            response = requests.get(f"{self.base_url}/api/consultas-medicas", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    consultas = data.get('data', [])
                    print(f"✅ API respondiendo correctamente")
                    print(f"📊 Consultas encontradas: {len(consultas)}")
                    
                    if consultas:
                        print("🔍 Última consulta:")
                        ultima = consultas[-1]
                        print(f"   ID: {ultima.get('id')}")
                        print(f"   Paciente: {ultima.get('paciente_nombre', 'N/A')}")
                        print(f"   Fecha: {ultima.get('fecha_consulta', 'N/A')}")
                        print(f"   Diagnóstico: {ultima.get('diagnostico', 'N/A')[:50]}...")
                    
                    return True
                else:
                    print(f"❌ API error: {data.get('error')}")
                    return False
            else:
                print(f"❌ HTTP error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error verificando API: {e}")
            return False
    
    def ejecutar_verificacion_completa(self):
        """Ejecutar verificación completa del sistema"""
        print("🎯 VERIFICACIÓN COMPLETA DEL SISTEMA MÉDICO")
        print("=" * 60)
        print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        resultados = {}
        
        # 1. Verificar BD
        resultados['bd'] = self.verificar_bd()
        
        # 2. Crear paciente
        if resultados['bd']:
            paciente_id = self.crear_paciente_prueba()
            resultados['paciente'] = paciente_id is not None
            
            # 3. Crear consulta
            if paciente_id:
                consulta_id = self.crear_consulta_prueba(paciente_id)
                resultados['consulta'] = consulta_id is not None
        
        # 4. Verificar API
        resultados['api'] = self.verificar_consultas_api()
        
        # Resumen final
        print("\n" + "=" * 60)
        print("📋 RESUMEN DE VERIFICACIÓN")
        print("=" * 60)
        
        total_tests = len(resultados)
        passed_tests = sum(resultados.values())
        
        for test, result in resultados.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test.upper()}")
        
        print(f"\n🎯 RESULTADO: {passed_tests}/{total_tests} pruebas exitosas")
        
        if passed_tests == total_tests:
            print("🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
            print("🔗 Listo para GitHub → Render")
        else:
            print("⚠️ Hay problemas que requieren atención")
        
        return passed_tests == total_tests

if __name__ == "__main__":
    verificador = VerificadorCompleto()
    verificador.ejecutar_verificacion_completa()