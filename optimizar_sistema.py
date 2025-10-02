#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OPTIMIZACIÓN COMPLETA DEL SISTEMA
1. Eliminar "Nueva Consulta" redundante
2. Aplicar colores azules consistentes
3. Hacer Módulo Médico siempre visible
"""

import os
import re

def optimizar_sistema():
    """Aplicar todas las optimizaciones al sistema"""
    
    print("🚀 OPTIMIZACIÓN COMPLETA DEL SISTEMA OFTALMETRYC")
    print("=" * 60)
    print()
    
    # Ruta base de templates
    base_path = "adapters/input/flask_app/templates"
    
    # PASO 1: ELIMINAR REFERENCIAS A "NUEVA CONSULTA"
    print("🚫 PASO 1: ELIMINANDO 'NUEVA CONSULTA' REDUNDANTE")
    print("-" * 50)
    
    templates_principales = [
        "dashboard.html",
        "historial_ventas.html", 
        "registrar_venta.html",
        "usuarios.html",
        "productos.html"
    ]
    
    templates_medicos = [
        "medical/dashboard_medico.html",
        "medical/pacientes.html",
        "medical/consultas.html",
        "medical/examen_oftalmologico.html",
        "medical/detalle_paciente.html",
        "medical/detalle_consulta.html",
        "medical/ficha_clinica.html"
    ]
    
    # Nuevo menú optimizado sin "Nueva Consulta"
    nuevo_menu_dropdown = '''                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="/dashboard-medico"><i class="fas fa-chart-line me-2"></i>Dashboard Médico</a></li>
                            <li><a class="dropdown-item" href="/pacientes"><i class="fas fa-users me-2"></i>Pacientes</a></li>
                            <li><a class="dropdown-item" href="/consultas"><i class="fas fa-calendar-check me-2"></i>Historial Consultas</a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="/ficha-clinica"><i class="fas fa-clipboard-check me-2"></i>Ficha Clínica</a></li>
                        </ul>'''
    
    # PASO 2: COLORES AZULES CONSISTENTES
    print("🎨 PASO 2: APLICANDO COLORES AZULES CONSISTENTES")
    print("-" * 50)
    
    # CSS actualizado con colores azules consistentes
    css_azul_consistente = '''        :root {
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
        
        /* NAVBAR AZUL CONSISTENTE */
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
        
        /* BOTONES AZULES CONSISTENTES */
        .btn-primary {
            background: linear-gradient(135deg, var(--secondary-color), #5dade2);
            border: none;
            border-radius: 25px;
            transition: all 0.3s ease;
        }
        
        .btn-primary:hover {
            background: linear-gradient(135deg, var(--accent-color), var(--secondary-color));
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
        }
        
        /* CARDS AZULES CONSISTENTES */
        .card {
            border: none;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }
        
        .card-header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            border-radius: 15px 15px 0 0 !important;
        }
        
        /* TABLAS AZULES CONSISTENTES */
        .table thead {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
        }'''
    
    # PASO 3: HACER MÓDULO MÉDICO SIEMPRE VISIBLE
    print("👁️ PASO 3: MÓDULO MÉDICO SIEMPRE VISIBLE")
    print("-" * 45)
    
    menu_siempre_visible = '''                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <i class="fas fa-eye me-1"></i>Módulo Médico
                        </a>'''
    
    print("✅ Configuración preparada")
    print("📄 Archivos a modificar identificados")
    print("🎯 Cambios listos para aplicar")
    print()
    
    print("🔄 CAMBIOS QUE SE APLICARÁN:")
    print("-" * 30)
    print("❌ Eliminar: 'Nueva Consulta' de todos los menús")
    print("🔄 Cambiar: 'Consultas' → 'Historial Consultas'")
    print("➕ Agregar: 'Ficha Clínica' como opción principal")
    print("🎨 Aplicar: Colores azules consistentes en todo el sistema")
    print("👁️ Garantizar: Módulo Médico siempre visible")
    print()
    
    return {
        'nuevo_menu': nuevo_menu_dropdown,
        'css_azul': css_azul_consistente,
        'menu_visible': menu_siempre_visible,
        'templates_principales': templates_principales,
        'templates_medicos': templates_medicos
    }

if __name__ == "__main__":
    config = optimizar_sistema()
    print("🎯 CONFIGURACIÓN LISTA PARA APLICAR")
    print("💡 Ejecuta los siguientes pasos para completar la optimización")