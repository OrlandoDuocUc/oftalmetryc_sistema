from flask import jsonify, request
from app.domain.use_cases.services.paciente_service import PacienteService

class PacienteController:
    def __init__(self):
        self.paciente_service = PacienteService()
    
    def get_all_pacientes(self):
        """Obtiene todos los pacientes"""
        try:
            pacientes = self.paciente_service.get_all_pacientes()
            return jsonify({
                'success': True,
                'data': pacientes,
                'total': len(pacientes)
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def get_paciente_by_id(self, paciente_id):
        """Obtiene un paciente por ID"""
        try:
            paciente = self.paciente_service.get_paciente_by_id(paciente_id)
            if paciente:
                return jsonify({
                    'success': True,
                    'data': paciente
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Paciente no encontrado'
                }), 404
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def search_pacientes(self):
        """Busca pacientes"""
        try:
            query = request.args.get('q', '')
            pacientes = self.paciente_service.search_pacientes(query)
            return jsonify({
                'success': True,
                'data': pacientes,
                'total': len(pacientes)
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def create_paciente(self):
        """Crea un nuevo paciente"""
        try:
            data = request.get_json()
            
            # Validaciones básicas
            if not data.get('rut') or not data.get('nombre') or not data.get('apellido'):
                return jsonify({
                    'success': False,
                    'error': 'RUT, nombre y apellido son obligatorios'
                }), 400
            
            # Validar RUT
            if not self.paciente_service.validate_rut(data['rut']):
                return jsonify({
                    'success': False,
                    'error': 'RUT inválido'
                }), 400
            
            paciente = self.paciente_service.create_paciente(data)
            if paciente:
                return jsonify({
                    'success': True,
                    'data': paciente,
                    'message': 'Paciente creado exitosamente'
                }), 201
            else:
                return jsonify({
                    'success': False,
                    'error': 'Error al crear paciente'
                }), 500
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def update_paciente(self, paciente_id):
        """Actualiza un paciente existente"""
        try:
            data = request.get_json()
            
            # Validar RUT si se está actualizando
            if 'rut' in data and not self.paciente_service.validate_rut(data['rut']):
                return jsonify({
                    'success': False,
                    'error': 'RUT inválido'
                }), 400
            
            paciente = self.paciente_service.update_paciente(paciente_id, data)
            if paciente:
                return jsonify({
                    'success': True,
                    'data': paciente,
                    'message': 'Paciente actualizado exitosamente'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Paciente no encontrado'
                }), 404
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def delete_paciente(self, paciente_id):
        """Elimina un paciente"""
        try:
            success = self.paciente_service.delete_paciente(paciente_id)
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Paciente eliminado exitosamente'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Paciente no encontrado'
                }), 404
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500