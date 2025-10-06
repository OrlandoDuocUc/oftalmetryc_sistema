# RUTAS DEL MÓDULO MÉDICO - ENDPOINTS PARA LOS NUEVOS TEMPLATES

# Estas rutas deben ser añadidas al archivo de rutas principal de Flask

@app.route('/dashboard-medico')
def dashboard_medico():
    """Dashboard principal del módulo médico con sidebar fijo"""
    return render_template('medical/dashboard_medico_final.html')

@app.route('/pacientes-nuevo')
def pacientes_nuevo():
    """Gestión de pacientes con navbar estándar"""
    return render_template('medical/pacientes_nuevo.html')

@app.route('/consultas-nuevo')
def consultas_nuevo():
    """Historial de consultas con navbar estándar"""
    return render_template('medical/consultas_nuevo.html')

@app.route('/ficha-clinica-nuevo')
def ficha_clinica_nuevo():
    """Formulario de ficha clínica con navbar estándar"""
    return render_template('medical/ficha_clinica_nuevo.html')

@app.route('/examen-oftalmologico-nuevo')
def examen_oftalmologico_nuevo():
    """Formulario de examen oftalmológico con navbar estándar"""
    return render_template('medical/examen_oftalmologico_nuevo.html')

# APIs para los formularios médicos

@app.route('/api/pacientes/<rut>', methods=['GET'])
def get_paciente_by_rut(rut):
    """API para buscar paciente por RUT"""
    try:
        # Implementar lógica de búsqueda de paciente
        # Este es un ejemplo, debe conectarse a la base de datos real
        return jsonify({
            'nombre': 'Ejemplo Paciente',
            'apellido': 'Apellido',
            'edad': 45,
            'telefono': '+56912345678'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/api/fichas-clinicas', methods=['POST'])
def crear_ficha_clinica():
    """API para guardar ficha clínica"""
    try:
        data = request.get_json()
        # Implementar lógica de guardado en base de datos
        return jsonify({'message': 'Ficha clínica guardada exitosamente', 'id': 1})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/examenes-oftalmologicos', methods=['POST'])
def crear_examen_oftalmologico():
    """API para guardar examen oftalmológico"""
    try:
        data = request.get_json()
        # Implementar lógica de guardado en base de datos
        return jsonify({'message': 'Examen oftalmológico guardado exitosamente', 'id': 1})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/consultas-medicas', methods=['GET'])
def get_consultas_medicas():
    """API para obtener lista de consultas médicas"""
    try:
        # Implementar lógica de consulta a base de datos
        # Este es un ejemplo, debe conectarse a la base de datos real
        consultas = [
            {
                'id': 1,
                'paciente_nombre': 'Juan Pérez',
                'fecha_consulta': '2024-01-15T10:30:00',
                'medico': 'María González',
                'estado': 'Completada'
            },
            {
                'id': 2,
                'paciente_nombre': 'Ana Silva',
                'fecha_consulta': '2024-01-15T14:00:00',
                'medico': 'Carlos Rodríguez',
                'estado': 'Pendiente'
            }
        ]
        return jsonify({'data': consultas})
    except Exception as e:
        return jsonify({'error': str(e)}), 500