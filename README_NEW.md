# 👓 Óptica Almonacid - Sistema de Gestión Oftalmológica

Sistema integral de gestión para ópticas con módulo médico especializado en oftalmología, desarrollado con Flask y PostgreSQL.

## 🌟 Características

- **Gestión de Ventas**: Control de productos, clientes y transacciones
- **Módulo Médico**: Sistema completo de historias clínicas oftalmológicas
- **Exámenes Especializados**: Biomicroscopía, oftalmoscopía, agudeza visual
- **Adaptado para Ecuador**: Validación de cédula y formatos locales
- **Responsive Design**: Interfaz moderna con Bootstrap 5

## 🚀 Demo en Vivo

La aplicación está desplegada en Render: [URL se generará automáticamente]

**Credenciales de prueba:**
- Usuario: `admin`
- Contraseña: `admin123`

## 📋 Funcionalidades

### Módulo de Ventas
- ✅ Gestión de productos y stock
- ✅ Registro de ventas y clientes
- ✅ Dashboard con métricas
- ✅ Historial de transacciones

### Módulo Médico
- ✅ Gestión de pacientes (adaptado para Ecuador)
- ✅ Consultas oftalmológicas completas
- ✅ Exámenes básicos y especializados
- ✅ Diagnósticos con códigos CIE-10
- ✅ Recetas oftalmológicas
- ✅ Programación de citas

## 🛠️ Tecnologías

- **Backend**: Flask 3.1.1, SQLAlchemy
- **Frontend**: Bootstrap 5, JavaScript ES6
- **Base de Datos**: PostgreSQL
- **Deploy**: Render
- **Arquitectura**: Hexagonal (Clean Architecture)

## 🌍 Deploy en Render

### Configuración Automática

1. **Fork este repositorio** en tu cuenta de GitHub

2. **Conectar con Render**:
   - Ve a [render.com](https://render.com)
   - Conecta tu cuenta de GitHub
   - Selecciona este repositorio

3. **Variables de Entorno** (se configuran automáticamente):
   ```
   FLASK_ENV=production
   SECRET_KEY=[generada automáticamente]
   DATABASE_URL=[proporcionada por PostgreSQL]
   ```

4. **Deploy automático**: Render detectará el `render.yaml` y creará:
   - Servicio web Python
   - Base de datos PostgreSQL
   - Inicialización automática

## 🔧 Desarrollo Local

### Prerrequisitos
- Python 3.8+
- PostgreSQL
- Git

### Instalación

1. **Clonar repositorio**:
   ```bash
   git clone https://github.com/sofiadonosoalarcon/optica-maipu.git
   cd optica-maipu
   ```

2. **Crear entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # o
   venv\Scripts\activate     # Windows
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar base de datos**:
   ```bash
   # Crear base de datos PostgreSQL
   createdb optica_db
   
   # Ejecutar script de inicialización
   python init_db.py
   ```

5. **Variables de entorno**:
   ```bash
   cp .env.example .env
   # Editar .env con tus configuraciones
   ```

6. **Ejecutar aplicación**:
   ```bash
   python boot.py
   ```

## 👥 Credenciales de Demo

Para facilitar las pruebas, el sistema incluye usuarios por defecto:

- **Administrador**: `admin` / `admin123`
- **Vendedor**: `vendedor` / `vendedor123`

## 📊 Estructura del Proyecto

```
optica-maipu/
├── adapters/
│   ├── input/flask_app/       # Capa de presentación
│   └── output/repositories/   # Acceso a datos
├── app/
│   ├── domain/models/         # Entidades de negocio
│   ├── domain/use_cases/      # Casos de uso
│   └── infrastructure/        # Implementaciones
├── config/                    # Configuraciones
├── medical_tables.sql         # Schema de base de datos
├── render.yaml               # Configuración de Render
└── requirements.txt          # Dependencias
```

## 🔐 Seguridad

- Validación de entrada en frontend y backend
- Protección contra inyección SQL con SQLAlchemy
- Manejo seguro de sesiones
- Variables de entorno para credenciales

## 📞 Soporte

Para soporte técnico o consultas sobre el sistema.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

---

**Desarrollado con ❤️ para Óptica Almonacid**