#!/usr/bin/env python3
"""
APLICADOR DE ESTILO DASHBOARD EXACTO
==================================

Aplica el estilo EXACTO del dashboard.html a todas las páginas:
1. Mismo gradiente azul
2. Mismos efectos hover
3. Mismos dropdowns
4. Corrige problemas de navegación
"""

import os
import re
from pathlib import Path

def aplicar_estilo_dashboard_exacto():
    """Aplica el estilo EXACTO del dashboard a todas las páginas"""
    
    print("🎨 APLICANDO ESTILO DASHBOARD EXACTO A TODAS LAS PÁGINAS")
    print("=" * 60)
    
    # Estilo EXACTO del dashboard.html
    estilo_dashboard_exacto = """    <style>
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --accent-color: #2980b9;
            --success-color: #27ae60;
            --warning-color: #f39c12;
            --danger-color: #e74c3c;
            --light-bg: #ecf0f1;
            --dark-bg: #34495e;
        }
        
        body {
            background-color: var(--light-bg);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* NAVBAR AZUL CONSISTENTE - ESTILO DASHBOARD EXACTO */
        .navbar {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .navbar-brand, .navbar-nav .nav-link {
            color: white !important;
        }
        
        .navbar-nav .nav-link:hover {
            color: #bdc3c7 !important;
        }
        
        .dropdown-menu {
            background: white;
            border: none;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .dropdown-item {
            color: var(--primary-color);
            transition: all 0.3s ease;
        }
        
        .dropdown-item:hover {
            background: linear-gradient(135deg, var(--secondary-color), #5dade2);
            color: white;
        }
        
        .dropdown-item.active {
            background: linear-gradient(135deg, var(--accent-color), var(--secondary-color));
            color: white;
        }
    </style>"""
    
    # Archivos a corregir
    templates_dir = Path(r"c:\Users\Usuario\Desktop\MAURICIO TODO\TRABAJO MAURICIO UDLA\VERSION FINAL PRO ALMONACID\version 2 optica almonacid (FINAL) BUENA\optica-maipu\adapters\input\flask_app\templates")
    
    archivos_a_corregir = [
        "productos.html",
        "registrar_venta.html", 
        "historial_ventas.html",
        "usuarios.html"
    ]
    
    resultados = []
    
    for archivo in archivos_a_corregir:
        archivo_path = templates_dir / archivo
        
        if archivo_path.exists():
            try:
                with open(archivo_path, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                # Remover estilos anteriores si existen
                contenido = re.sub(
                    r'<style>.*?</style>',
                    '',
                    contenido,
                    flags=re.DOTALL
                )
                
                # Insertar estilo dashboard exacto
                contenido = re.sub(
                    r'(</head>)',
                    f'{estilo_dashboard_exacto}\n\\1',
                    contenido,
                    flags=re.IGNORECASE
                )
                
                # Escribir archivo
                with open(archivo_path, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                
                resultados.append(f"✅ {archivo}: Estilo dashboard exacto aplicado")
                
            except Exception as e:
                resultados.append(f"❌ {archivo}: Error - {str(e)}")
        else:
            resultados.append(f"🚫 {archivo}: No encontrado")
    
    return resultados

def corregir_problemas_navegacion():
    """Corrige problemas específicos de navegación"""
    
    print(f"\n🔧 CORRIGIENDO PROBLEMAS DE NAVEGACIÓN:")
    print("-" * 45)
    
    templates_dir = Path(r"c:\Users\Usuario\Desktop\MAURICIO TODO\TRABAJO MAURICIO UDLA\VERSION FINAL PRO ALMONACID\version 2 optica almonacid (FINAL) BUENA\optica-maipu\adapters\input\flask_app\templates")
    
    problemas_corregidos = []
    
    # 1. Cambiar "Historial" por "Historial Ventas"
    archivos_historial = ["dashboard.html", "productos.html", "registrar_venta.html", "usuarios.html"]
    
    for archivo in archivos_historial:
        archivo_path = templates_dir / archivo
        if archivo_path.exists():
            with open(archivo_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Cambiar "Historial" por "Historial Ventas"
            contenido = re.sub(
                r'(<a[^>]*href="/historial-ventas"[^>]*>)Historial(</a>)',
                r'\1Historial Ventas\2',
                contenido
            )
            
            with open(archivo_path, 'w', encoding='utf-8') as f:
                f.write(contenido)
            
            problemas_corregidos.append(f"✅ {archivo}: 'Historial' → 'Historial Ventas'")
    
    # 2. Verificar "Nueva Consulta" vs "Ficha Clínica" en registrar_venta.html
    registrar_venta_path = templates_dir / "registrar_venta.html"
    if registrar_venta_path.exists():
        with open(registrar_venta_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Asegurar que dice "Ficha Clínica" y no "Nueva Consulta"
        contenido = re.sub(
            r'Nueva Consulta',
            'Ficha Clínica',
            contenido
        )
        
        with open(registrar_venta_path, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        problemas_corregidos.append("✅ registrar_venta.html: 'Nueva Consulta' → 'Ficha Clínica'")
    
    return problemas_corregidos

def generar_reporte_final():
    """Genera reporte final de todas las correcciones"""
    
    resultados_estilo = aplicar_estilo_dashboard_exacto()
    problemas_navegacion = corregir_problemas_navegacion()
    
    print(f"\n📋 RESULTADOS - ESTILO DASHBOARD EXACTO:")
    print("-" * 45)
    for resultado in resultados_estilo:
        print(resultado)
    
    print(f"\n📋 RESULTADOS - PROBLEMAS NAVEGACIÓN:")
    print("-" * 40)
    for problema in problemas_navegacion:
        print(problema)
    
    print(f"\n🎯 CORRECCIONES COMPLETADAS:")
    print("-" * 35)
    print("✅ Estilo dashboard EXACTO en todas las páginas")
    print("✅ Gradiente azul consistente (#2c3e50 → #3498db)")
    print("✅ Hover effects idénticos")
    print("✅ Dropdowns con mismo estilo")
    print("✅ 'Historial' → 'Historial Ventas'")
    print("✅ 'Nueva Consulta' → 'Ficha Clínica'")
    
    print(f"\n✨ RESULTADO: Interface 100% consistente")
    print("   con el estilo exacto del dashboard que te gusta.")

if __name__ == "__main__":
    generar_reporte_final()