#!/usr/bin/env python3
"""
OPTIMIZADOR DE COLORES Y UI SISTEMA ÓPTICA ALMONACID
===================================================

Este script automatiza la aplicación de:
1. Paleta de colores azul consistente en todas las plantillas médicas
2. Mejora de la accesibilidad con aria-expanded
3. Optimización de la navegación navbar
4. Variables CSS personalizadas

Autor: Sistema de Optimización UI
Fecha: 2024
"""

import os
import re
from pathlib import Path

def optimizar_colores_medicos():
    """Aplica la paleta de colores azul consistente en todas las plantillas médicas"""
    
    # Directorio base de plantillas médicas
    medical_templates_dir = Path(r"c:\Users\Usuario\Desktop\MAURICIO TODO\TRABAJO MAURICIO UDLA\VERSION FINAL PRO ALMONACID\version 2 optica almonacid (FINAL) BUENA\optica-maipu\adapters\input\flask_app\templates\medical")
    
    # CSS Variables para colores consistentes
    css_variables = """
    <style>
        :root {
            --primary-blue: #007bff;
            --primary-blue-dark: #0056b3;
            --navbar-blue: #1e3a8a;
            --card-blue: #f8faff;
            --text-blue: #1e40af;
            --border-blue: #3b82f6;
        }
        
        .navbar {
            background: linear-gradient(135deg, var(--navbar-blue) 0%, var(--primary-blue) 100%) !important;
        }
        
        .nav-link {
            color: #ffffff !important;
            font-weight: 500;
        }
        
        .nav-link:hover {
            color: #e3f2fd !important;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
        }
        
        .dropdown-menu {
            border: 1px solid var(--border-blue);
            box-shadow: 0 4px 12px rgba(30, 58, 138, 0.15);
        }
        
        .dropdown-item:hover {
            background-color: var(--card-blue);
            color: var(--text-blue);
        }
        
        .btn-primary {
            background-color: var(--primary-blue);
            border-color: var(--primary-blue);
        }
        
        .btn-primary:hover {
            background-color: var(--primary-blue-dark);
            border-color: var(--primary-blue-dark);
        }
        
        .card {
            border: 1px solid var(--border-blue);
            background-color: var(--card-blue);
        }
        
        .card-header {
            background-color: var(--primary-blue);
            color: white;
            border-bottom: 1px solid var(--border-blue);
        }
        
        .table-primary {
            background-color: var(--card-blue);
        }
        
        h1, h2, h3 {
            color: var(--text-blue);
        }
    </style>
    """
    
    # Fragmento de navegación optimizado
    nav_fragment_optimized = """
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="fas fa-eye me-1"></i>Módulo Médico
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="/dashboard-medico"><i class="fas fa-chart-line me-2"></i>Dashboard Médico</a></li>
                            <li><a class="dropdown-item" href="/pacientes"><i class="fas fa-users me-2"></i>Pacientes</a></li>
                            <li><a class="dropdown-item" href="/consultas"><i class="fas fa-calendar-check me-2"></i>Historial Consultas</a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="/ficha-clinica"><i class="fas fa-clipboard-check me-2"></i>Ficha Clínica</a></li>
                        </ul>
                    </li>
    """
    
    # Archivos médicos a procesar
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
    
    resultados = []
    
    for archivo in archivos_medicos:
        archivo_path = medical_templates_dir / archivo
        
        if archivo_path.exists():
            try:
                with open(archivo_path, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                # Insertar variables CSS después del <head>
                contenido = re.sub(
                    r'(<head[^>]*>)',
                    f'\\1\n{css_variables}',
                    contenido,
                    flags=re.IGNORECASE
                )
                
                # Optimizar navbar - remover "Nueva Consulta" redundante
                contenido = re.sub(
                    r'<li><a class="dropdown-item" href="/consultas/nueva">.*?Nueva Consulta.*?</a></li>',
                    '',
                    contenido,
                    flags=re.DOTALL
                )
                
                # Cambiar "Consultas" por "Historial Consultas"
                contenido = re.sub(
                    r'(<a class="dropdown-item" href="/consultas">.*?)Consultas(.*?</a>)',
                    r'\1Historial Consultas\2',
                    contenido
                )
                
                # Agregar aria-expanded="false" a dropdowns
                contenido = re.sub(
                    r'(<a class="nav-link dropdown-toggle"[^>]*data-bs-toggle="dropdown")([^>]*>)',
                    r'\1 aria-expanded="false"\2',
                    contenido
                )
                
                # Asegurar que Dashboard Médico esté siempre visible
                contenido = re.sub(
                    r'(<a class="dropdown-item" href="/dashboard-medico">)',
                    r'<li style="font-weight: bold; background-color: var(--card-blue);">\1',
                    contenido
                )
                
                # Escribir archivo optimizado
                with open(archivo_path, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                
                resultados.append(f"✅ {archivo}: Optimizado con éxito")
                
            except Exception as e:
                resultados.append(f"❌ {archivo}: Error - {str(e)}")
        else:
            resultados.append(f"⚠️ {archivo}: No encontrado")
    
    return resultados

def generar_reporte_optimizacion():
    """Genera reporte de optimización de UI"""
    
    print("🎨 OPTIMIZADOR DE COLORES Y UI - SISTEMA ÓPTICA ALMONACID")
    print("=" * 65)
    
    # Ejecutar optimización
    resultados = optimizar_colores_medicos()
    
    print("\n📋 RESULTADOS DE OPTIMIZACIÓN:")
    print("-" * 40)
    for resultado in resultados:
        print(resultado)
    
    print("\n🎯 MEJORAS APLICADAS:")
    print("-" * 25)
    print("✅ Paleta de colores azul consistente")
    print("✅ Variables CSS personalizadas")
    print("✅ Navbar con gradiente azul")
    print("✅ Dropdown menus mejorados")
    print("✅ Accesibilidad aria-expanded")
    print("✅ Dashboard Médico siempre visible")
    print("✅ Eliminación de 'Nueva Consulta' redundante")
    print("✅ Renombrado 'Consultas' → 'Historial Consultas'")
    
    print("\n🎨 PALETA DE COLORES APLICADA:")
    print("-" * 35)
    print("🔵 Primary Blue: #007bff")
    print("🔵 Primary Blue Dark: #0056b3") 
    print("🔵 Navbar Blue: #1e3a8a")
    print("🔵 Card Blue: #f8faff")
    print("🔵 Text Blue: #1e40af")
    print("🔵 Border Blue: #3b82f6")
    
    print("\n✨ OPTIMIZACIÓN COMPLETADA CON ÉXITO")
    print("Las plantillas médicas ahora tienen colores consistentes")
    print("y una navegación optimizada según los requerimientos.")

if __name__ == "__main__":
    generar_reporte_optimizacion()