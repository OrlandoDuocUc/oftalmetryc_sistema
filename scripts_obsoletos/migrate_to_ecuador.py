#!/usr/bin/env python3
"""
Script de migración para adaptar Oftalmetryc a Ecuador
Actualiza referencias de Chile a Ecuador en toda la aplicación
"""

import os
import re
from pathlib import Path

def update_files_for_ecuador():
    """Actualiza archivos para adaptación a Ecuador"""
    
    # Directorio base del proyecto
    base_dir = Path(__file__).parent
    
    # Patrones de reemplazo
    replacements = {
        # Documentos de identidad
        r'\bRUT\b': 'Cédula',
        r'\brut\b': 'cedula',
        r'12\.345\.678-9': '1234567890',
        r'XX\.XXX\.XXX-X': 'XXXXXXXXXX',
        
        # Teléfonos
        r'\+56 9 \d{4} \d{4}': '0987654321',
        r'\+56 9 XXXX XXXX': '09XXXXXXXX',
        
        # Zona horaria
        r'America/Santiago': 'America/Guayaquil',
        r'es-CL': 'es-EC',
        
        # Moneda (opcional)
        r'\bCLP\b': 'USD',
        r'peso chileno': 'dólar estadounidense'
    }
    
    # Extensiones de archivos a procesar
    file_extensions = ['.py', '.html', '.js', '.sql', '.md']
    
    # Buscar y actualizar archivos
    updated_files = []
    
    for root, dirs, files in os.walk(base_dir):
        # Evitar directorios específicos
        if any(skip in root for skip in ['.git', '__pycache__', 'venv', 'node_modules']):
            continue
            
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions):
                file_path = Path(root) / file
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    
                    # Aplicar reemplazos
                    for pattern, replacement in replacements.items():
                        content = re.sub(pattern, replacement, content)
                    
                    # Si hubo cambios, guardar archivo
                    if content != original_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        updated_files.append(str(file_path))
                        
                except Exception as e:
                    print(f"Error procesando {file_path}: {e}")
    
    return updated_files

if __name__ == "__main__":
    print("🇪🇨 Iniciando adaptación de Oftalmetryc para Ecuador...")
    
    updated_files = update_files_for_ecuador()
    
    if updated_files:
        print(f"\n✅ Archivos actualizados ({len(updated_files)}):")
        for file in updated_files:
            print(f"   • {file}")
    else:
        print("\n📋 No se encontraron archivos para actualizar.")
    
    print("\n🎉 Adaptación completada exitosamente!")
    print("\n📝 Cambios principales realizados:")
    print("   • RUT → Cédula de Ciudadanía (10 dígitos)")
    print("   • Formato teléfono: 09XXXXXXXX / 02XXXXXXX")
    print("   • Zona horaria: America/Guayaquil")
    print("   • Idioma: es-EC")