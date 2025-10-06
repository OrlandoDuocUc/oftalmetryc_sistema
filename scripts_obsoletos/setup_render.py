#!/usr/bin/env python3
"""
CONFIGURACIÓN AUTOMÁTICA PARA RENDER
Se ejecuta automáticamente cuando se hace deploy en Render
"""
import os
import sys
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_render_environment():
    """Configurar entorno automáticamente en Render"""
    logger.info("🚀 CONFIGURACIÓN AUTOMÁTICA PARA RENDER")
    logger.info("=" * 50)
    
    # Verificar si estamos en Render
    if 'RENDER' in os.environ:
        logger.info("🌐 Detectado entorno de Render")
        
        # Ejecutar migraciones automáticas
        try:
            from migrations.auto_migrate import AutoMigrationSystem
            migrator = AutoMigrationSystem()
            success = migrator.run_migrations()
            
            if success:
                logger.info("✅ Migraciones aplicadas exitosamente")
            else:
                logger.error("❌ Error en migraciones")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error ejecutando migraciones: {e}")
            return False
    
    else:
        logger.info("🏠 Entorno local detectado")
        # En local, también aplicar migraciones para mantener sincronía
        try:
            from migrations.auto_migrate import AutoMigrationSystem
            migrator = AutoMigrationSystem()
            success = migrator.run_migrations()
            
            if success:
                logger.info("✅ Base de datos local sincronizada")
            else:
                logger.error("❌ Error sincronizando base de datos local")
        except Exception as e:
            logger.error(f"⚠️ Advertencia en sincronización local: {e}")
    
    return True

if __name__ == "__main__":
    setup_render_environment()