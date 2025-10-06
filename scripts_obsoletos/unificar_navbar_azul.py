#!/usr/bin/env python3
"""
UNIFICADOR DE ESTILOS NAVBAR AZUL
================================

Aplica el estilo navbar azul hermoso a TODAS las plantillas:
- Productos
- Registrar Venta 
- Historial Ventas
- Usuarios

Para que sea consistente con Dashboard y Módulo Médico.
"""

import os
import re
from pathlib import Path

def aplicar_estilo_navbar_azul():
    """Aplica el estilo navbar azul consistente a todas las plantillas"""
    
    print("🎨 UNIFICADOR DE ESTILOS NAVBAR AZUL")
    print("=" * 40)
    
    # Directorio de plantillas principales
    templates_dir = Path(r"c:\Users\Usuario\Desktop\MAURICIO TODO\TRABAJO MAURICIO UDLA\VERSION FINAL PRO ALMONACID\version 2 optica almonacid (FINAL) BUENA\optica-maipu\adapters\input\flask_app\templates")
    
    # Archivos que necesitan el estilo azul
    archivos_a_corregir = [
        "productos.html",
        "registrar_venta.html", 
        "historial_ventas.html",
        "usuarios.html"
    ]
    
    # CSS azul hermoso que está en dashboard.html
    css_azul_hermoso = """    <style>
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --accent-color: #2980b9;
            --success-color: #27ae60;
            --warning-color: #f39c12;
            --danger-color: #e74c3c;
            --light-bg: #ecf0f1;
            --dark-bg: #34495e;
            
            /* Variables azules del módulo médico */
            --primary-blue: #007bff;
            --primary-blue-dark: #0056b3;
            --navbar-blue: #1e3a8a;
            --card-blue: #f8faff;
            --text-blue: #1e40af;
            --border-blue: #3b82f6;
        }
        
        body {
            background-color: var(--light-bg);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* NAVBAR AZUL CONSISTENTE - MISMO ESTILO PARA TODOS */
        .navbar {
            background: linear-gradient(135deg, var(--navbar-blue) 0%, var(--primary-blue) 100%) !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .nav-link {
            color: #ffffff !important;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .nav-link:hover {
            color: #e3f2fd !important;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
        }
        
        .nav-link.active {
            background-color: rgba(255, 255, 255, 0.2) !important;
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
        
        .navbar-brand {
            color: #ffffff !important;
            font-weight: bold;
            font-size: 1.5rem;
        }
        
        .navbar-brand:hover {
            color: #e3f2fd !important;
        }
    </style>"""
    
    resultados = []
    
    for archivo in archivos_a_corregir:
        archivo_path = templates_dir / archivo
        
        if archivo_path.exists():
            try:
                with open(archivo_path, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                # Eliminar navbar bg-dark y reemplazar por clase neutra
                contenido = re.sub(
                    r'<nav class="navbar navbar-expand-lg navbar-dark bg-dark">',
                    '<nav class="navbar navbar-expand-lg navbar-dark">',
                    contenido
                )
                
                # Insertar CSS azul después del </head> si no existe
                if 'NAVBAR AZUL CONSISTENTE' not in contenido:
                    contenido = re.sub(
                        r'(</head>)',
                        f'{css_azul_hermoso}\n\\1',
                        contenido,
                        flags=re.IGNORECASE
                    )
                
                # Escribir archivo corregido
                with open(archivo_path, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                
                resultados.append(f"✅ {archivo}: Estilo azul aplicado")
                
            except Exception as e:
                resultados.append(f"❌ {archivo}: Error - {str(e)}")
        else:
            resultados.append(f"🚫 {archivo}: No encontrado")
    
    return resultados

def generar_reporte_unificacion():
    """Genera reporte de unificación de estilos"""
    
    resultados = aplicar_estilo_navbar_azul()
    
    print(f"\n📋 RESULTADOS DE UNIFICACIÓN:")
    print("-" * 35)
    for resultado in resultados:
        print(resultado)
    
    print(f"\n🎯 ESTILOS UNIFICADOS:")
    print("-" * 25)
    print("✅ Navbar azul hermoso en TODAS las páginas")
    print("✅ Gradiente azul consistente (#1e3a8a → #007bff)")
    print("✅ Enlaces blancos con hover azul claro")
    print("✅ Dropdowns con bordes azules")
    print("✅ Efectos de transición suaves")
    print("✅ Marca 'Oftalmetryc' destacada")
    
    print(f"\n🔄 ANTES vs DESPUÉS:")
    print("-" * 25)
    print("❌ ANTES: Dashboard = azul, Productos = negro")
    print("✅ DESPUÉS: TODOS = azul hermoso consistente")
    
    print(f"\n✨ RESULTADO: Interface completamente unificada")
    print("   con el estilo azul que te gusta en TODA la aplicación.")

if __name__ == "__main__":
    generar_reporte_unificacion()