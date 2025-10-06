#!/usr/bin/env python3
"""
Script para convertir todos los templates del módulo médico a herencia de base.html
Automatiza la conversión del navbar unificado para todos los templates médicos
"""

import os
import re
from pathlib import Path

# Ruta base de los templates médicos
MEDICAL_TEMPLATES_DIR = r"c:\Users\Usuario\Desktop\MAURICIO TODO\TRABAJO MAURICIO UDLA\VERSION FINAL PRO ALMONACID\version 2 optica almonacid (FINAL) BUENA\optica-maipu\adapters\input\flask_app\templates\medical"

# Templates que deben ser convertidos (basado en el análisis de las rutas)
TEMPLATES_TO_CONVERT = [
    "dashboard_medico.html",  # Ya iniciado
    "pacientes.html",         # Ya iniciado  
    "nuevo_paciente.html",
    "detalle_paciente.html", 
    "consultas.html",
    "detalle_consulta.html",
    "examen_oftalmologico.html",
    "ficha_clinica.html"
]

def extract_title_from_template(file_path):
    """Extrae el título del template original"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Buscar el título en el <title> tag
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        if title_match:
            return title_match.group(1).strip()
        
        # Fallback: crear título basado en el nombre del archivo
        filename = os.path.basename(file_path).replace('.html', '').replace('_', ' ').title()
        return f"{filename} - Oftalmetryc"
        
    except Exception as e:
        print(f"Error extrayendo título de {file_path}: {e}")
        return "Módulo Médico - Oftalmetryc"

def extract_styles_from_template(file_path):
    """Extrae los estilos específicos del template (sin navbar styles)"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Buscar el bloque <style>
        style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL | re.IGNORECASE)
        if style_match:
            styles = style_match.group(1).strip()
            
            # Filtrar estilos del navbar (queremos mantener solo estilos específicos)
            # Eliminar estilos relacionados con navbar, nav-link, dropdown-menu, etc.
            lines = styles.split('\n')
            filtered_lines = []
            skip_block = False
            
            for line in lines:
                line_clean = line.strip()
                
                # Definir patrones de estilos a omitir (navbar y elementos del nav)
                skip_patterns = [
                    'navbar', 'nav-link', 'dropdown-menu', 'dropdown-item',
                    ':root {', '--navbar-', '--primary-blue', '--card-blue',
                    'background: linear-gradient(135deg, var(--navbar'
                ]
                
                # Si encontramos un patrón a omitir, saltar este bloque
                should_skip = any(pattern in line_clean for pattern in skip_patterns)
                
                if '{' in line and should_skip:
                    skip_block = True
                elif '}' in line and skip_block:
                    skip_block = False
                    continue
                elif not skip_block and not should_skip:
                    filtered_lines.append(line)
            
            return '\n'.join(filtered_lines).strip()
        
        return "/* Estilos específicos del template */"
        
    except Exception as e:
        print(f"Error extrayendo estilos de {file_path}: {e}")
        return "/* Error al extraer estilos */"

def extract_content_from_template(file_path):
    """Extrae el contenido principal del template (sin navbar y estructura HTML base)"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar el contenido después del navbar
        # Buscar patrones comunes de inicio de contenido
        patterns = [
            r'</nav>\s*<div class="container[^>]*>(.*?)</body>',
            r'</nav>\s*<div[^>]*>(.*?)</body>',
            r'<div class="container[^>]*>\s*<div class="row">(.*?)</body>',
            r'<div class="main-content[^>]*>(.*?)</body>',
            r'<!-- Main Content -->\s*<div[^>]*>(.*?)</body>'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                main_content = match.group(1).strip()
                
                # Limpiar scripts y cerrar tags
                main_content = re.sub(r'<script.*?</script>', '', main_content, flags=re.DOTALL)
                main_content = re.sub(r'</html>.*$', '', main_content, flags=re.DOTALL)
                
                return main_content.strip()
        
        # Fallback: buscar cualquier div container principal
        container_match = re.search(r'<div[^>]*class="[^"]*container[^"]*"[^>]*>(.*?)</div>', content, re.DOTALL)
        if container_match:
            return container_match.group(1).strip()
            
        return "<!-- Contenido no encontrado automáticamente -->"
        
    except Exception as e:
        print(f"Error extrayendo contenido de {file_path}: {e}")
        return "<!-- Error al extraer contenido -->"

def extract_scripts_from_template(file_path):
    """Extrae los scripts específicos del template"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar todos los scripts
        scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL | re.IGNORECASE)
        
        # Filtrar scripts (omitir Bootstrap y librerías comunes)
        custom_scripts = []
        for script in scripts:
            script_clean = script.strip()
            if script_clean and 'bootstrap' not in script_clean.lower() and 'cdn.jsdelivr' not in script_clean:
                custom_scripts.append(script_clean)
        
        return '\n'.join(custom_scripts).strip() if custom_scripts else "// Scripts específicos"
        
    except Exception as e:
        print(f"Error extrayendo scripts de {file_path}: {e}")
        return "// Error al extraer scripts"

def convert_template_to_inheritance(template_name):
    """Convierte un template específico a herencia de base.html"""
    file_path = os.path.join(MEDICAL_TEMPLATES_DIR, template_name)
    
    if not os.path.exists(file_path):
        print(f"❌ Template no encontrado: {file_path}")
        return False
    
    print(f"🔄 Convirtiendo: {template_name}")
    
    try:
        # Extraer componentes del template original
        title = extract_title_from_template(file_path)
        styles = extract_styles_from_template(file_path)
        content = extract_content_from_template(file_path)
        scripts = extract_scripts_from_template(file_path)
        
        # Crear el nuevo template con herencia
        new_template = f"""{% extends "base.html" %}

{% block title %}{title}{% endblock %}

{% block extra_css %}
{styles}
{% endblock %}

{% block content %}
<div class="container-fluid mt-4">
{content}
</div>
{% endblock %}

{% block extra_js %}
<script>
{scripts}
</script>
{% endblock %}"""

        # Escribir el nuevo template
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_template)
            
        print(f"✅ Convertido exitosamente: {template_name}")
        return True
        
    except Exception as e:
        print(f"❌ Error convirtiendo {template_name}: {e}")
        return False

def main():
    """Función principal para convertir todos los templates"""
    print("🚀 INICIANDO CONVERSIÓN DE TEMPLATES MÉDICOS")
    print("=" * 60)
    
    converted_count = 0
    failed_count = 0
    
    for template in TEMPLATES_TO_CONVERT:
        try:
            if convert_template_to_inheritance(template):
                converted_count += 1
            else:
                failed_count += 1
        except Exception as e:
            print(f"❌ Error general con {template}: {e}")
            failed_count += 1
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE CONVERSIÓN:")
    print(f"✅ Templates convertidos exitosamente: {converted_count}")
    print(f"❌ Templates fallidos: {failed_count}")
    print(f"📁 Total procesados: {len(TEMPLATES_TO_CONVERT)}")
    
    if converted_count == len(TEMPLATES_TO_CONVERT):
        print("\n🎉 ¡CONVERSIÓN COMPLETADA CON ÉXITO!")
        print("Todos los templates del módulo médico ahora usan el navbar unificado.")
    else:
        print(f"\n⚠️ Conversión parcial. Revisar templates fallidos.")

if __name__ == "__main__":
    main()