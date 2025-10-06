#!/usr/bin/env python3
"""
GUÍA DE DEPLOY MANUAL - SISTEMA ÓPTICA ALMONACID
===============================================

Esta guía te ayudará a hacer deploy manual de los cambios de UI 
optimizados desde GitHub hacia Render para ver las mejoras aplicadas.

Pasos para Deploy Manual:
1. Commit y Push de cambios locales a GitHub
2. Deploy manual desde Render Dashboard
3. Verificación de cambios aplicados

Autor: Sistema de Deploy
Fecha: 2024
"""

import subprocess
import os
from pathlib import Path

def verificar_git_status():
    """Verifica el estado actual del repositorio Git"""
    
    print("🔍 VERIFICANDO ESTADO DEL REPOSITORIO GIT")
    print("=" * 45)
    
    try:
        # Verificar estado de git
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            cambios = result.stdout.strip()
            if cambios:
                print("📝 ARCHIVOS MODIFICADOS PENDIENTES:")
                print("-" * 35)
                for linea in cambios.split('\n'):
                    if linea.strip():
                        estado = linea[:2]
                        archivo = linea[3:]
                        if 'M' in estado:
                            print(f"✏️  Modificado: {archivo}")
                        elif 'A' in estado:
                            print(f"➕ Agregado: {archivo}")
                        elif '??' in estado:
                            print(f"❓ Sin seguimiento: {archivo}")
                
                print(f"\n📊 Total archivos modificados: {len(cambios.split('\n'))}")
                return True
            else:
                print("✅ No hay cambios pendientes de commit")
                return False
        else:
            print("❌ Error al verificar estado de Git")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando git status: {str(e)}")
        return False

def generar_comandos_deploy():
    """Genera los comandos necesarios para el deploy"""
    
    print("\n🚀 COMANDOS PARA DEPLOY MANUAL")
    print("=" * 35)
    
    print("\n1️⃣ COMMIT Y PUSH DE CAMBIOS:")
    print("-" * 30)
    print("git add .")
    print('git commit -m "feat: Optimización UI - Colores azules consistentes y navegación mejorada"')
    print("git push origin main")
    
    print("\n2️⃣ DEPLOY MANUAL EN RENDER:")
    print("-" * 30)
    print("🌐 Ve a: https://dashboard.render.com/")
    print("📱 Busca tu servicio: 'oftalmetryc-sistema'")
    print("🔄 Haz clic en 'Manual Deploy' → 'Deploy latest commit'")
    print("⏱️  Espera 3-5 minutos hasta que complete")
    
    print("\n3️⃣ VERIFICAR CAMBIOS APLICADOS:")
    print("-" * 35)
    print("🌐 URL: https://oftalmetryc-sistema.onrender.com")
    print("👀 Verificar:")
    print("   • Navbar con colores azules")
    print("   • Dashboard Médico visible")
    print("   • 'Historial Consultas' en lugar de 'Consultas'")
    print("   • Sin opción 'Nueva Consulta' redundante")
    print("   • Colores consistentes en todo el sistema")

def mostrar_checklist_deploy():
    """Muestra checklist de verificación post-deploy"""
    
    print(f"\n✅ CHECKLIST POST-DEPLOY:")
    print("=" * 30)
    
    checklist = [
        "☐ Navbar tiene gradiente azul",
        "☐ Dashboard Médico está siempre visible",
        "☐ 'Consultas' se cambió a 'Historial Consultas'",
        "☐ Ya no aparece 'Nueva Consulta' redundante",
        "☐ Botones principales son azules",
        "☐ Cards tienen fondo azul claro",
        "☐ Enlaces y texto en tonos azules",
        "☐ Sin colores negros en la interfaz",
        "☐ Efectos hover funcionan correctamente",
        "☐ Menú dropdown accesible"
    ]
    
    for item in checklist:
        print(f"   {item}")
    
    print(f"\n📋 PÁGINAS A VERIFICAR:")
    print("-" * 25)
    paginas = [
        "🏠 Dashboard principal",
        "📦 Productos", 
        "📊 Historial Ventas",
        "💰 Registrar Venta",
        "👥 Usuarios",
        "🏥 Dashboard Médico",
        "👤 Pacientes",
        "📋 Historial Consultas",
        "📄 Ficha Clínica"
    ]
    
    for pagina in paginas:
        print(f"   {pagina}")

def ejecutar_git_commands():
    """Ejecuta los comandos de Git automáticamente"""
    
    print(f"\n🤖 EJECUTANDO COMANDOS GIT AUTOMÁTICAMENTE...")
    print("-" * 50)
    
    try:
        # git add .
        print("📝 Ejecutando: git add .")
        result = subprocess.run(['git', 'add', '.'], 
                              capture_output=True, text=True, cwd=os.getcwd())
        if result.returncode == 0:
            print("✅ git add . - Completado")
        else:
            print(f"❌ Error en git add: {result.stderr}")
            return False
        
        # git commit
        commit_msg = "feat: Optimización UI - Colores azules consistentes y navegación mejorada"
        print(f"💾 Ejecutando: git commit -m '{commit_msg}'")
        result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                              capture_output=True, text=True, cwd=os.getcwd())
        if result.returncode == 0:
            print("✅ git commit - Completado")
        else:
            print(f"⚠️ Commit info: {result.stdout}")
            if "nothing to commit" in result.stdout:
                print("ℹ️ No hay cambios nuevos para hacer commit")
        
        # git push
        print("🚀 Ejecutando: git push origin main")
        result = subprocess.run(['git', 'push', 'origin', 'main'], 
                              capture_output=True, text=True, cwd=os.getcwd())
        if result.returncode == 0:
            print("✅ git push - Completado")
            print("🎉 ¡Cambios subidos a GitHub exitosamente!")
            return True
        else:
            print(f"❌ Error en git push: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando comandos Git: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 GUÍA DE DEPLOY MANUAL - SISTEMA ÓPTICA ALMONACID")
    print("=" * 55)
    
    # Verificar cambios pendientes
    hay_cambios = verificar_git_status()
    
    if hay_cambios:
        print("\n🔄 ¿Deseas ejecutar los comandos Git automáticamente? (y/n)")
        respuesta = input("Respuesta: ").lower().strip()
        
        if respuesta in ['y', 'yes', 'sí', 'si', 's']:
            exito = ejecutar_git_commands()
            if exito:
                print("\n✅ ¡Git commands ejecutados exitosamente!")
                print("👉 Ahora ve a Render para hacer deploy manual")
        else:
            print("\n📋 Comandos manuales disponibles arriba")
    
    # Mostrar guía de deploy
    generar_comandos_deploy()
    mostrar_checklist_deploy()
    
    print(f"\n🎯 RESUMEN:")
    print("-" * 12)
    print("1. ✅ Optimizaciones UI aplicadas localmente")
    print("2. 🔄 Push cambios a GitHub (automático o manual)")
    print("3. 🚀 Deploy manual en Render dashboard")
    print("4. 👀 Verificar cambios en producción")
    
    print(f"\n🌐 URL FINAL: https://oftalmetryc-sistema.onrender.com")
    print("¡Disfruta tu nuevo diseño azul! 🎨✨")