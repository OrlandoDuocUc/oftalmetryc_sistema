'''

from flask import jsonify, request
from app.domain.use_cases.services.consulta_medica_service import ConsultaMedicaService

class ConsultaMedicaController:
    def __init__(self):
        self.consulta_service = ConsultaMedicaService()
    
    def get_all_consultas(self):
        """Obtiene todas las consultas médicas"""
        try:
            consultas = self.consulta_service.get_all_consultas()
            return jsonify({
                'success': True,
                'data': consultas,
                'total': len(consultas)
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def get_consulta_by_id(self, consulta_id):
        """Obtiene una consulta por ID"""
        try:
            consulta = self.consulta_service.get_consulta_by_id(consulta_id)
            if consulta:
                return jsonify({
                    'success': True,
                    'data': consulta
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Consulta no encontrada'
                }), 404
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def get_consultas_by_paciente(self, paciente_id):
        """Obtiene consultas de un paciente"""
        try:
            consultas = self.consulta_service.get_consultas_by_paciente(paciente_id)
            return jsonify({
                'success': True,
                'data': consultas,
                'total': len(consultas)
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def create_consulta(self):
        """Crea una nueva consulta médica"""
        try:
            data = request.get_json()
            
            # Validaciones básicas
            if not data.get('paciente_id'):
                return jsonify({
                    'success': False,
                    'error': 'ID del paciente es obligatorio'
                }), 400
            
            consulta = self.consulta_service.create_consulta(data)
            if consulta:
                return jsonify({
                    'success': True,
                    'data': consulta,
                    'message': 'Consulta creada exitosamente'
                }), 201
            else:
                return jsonify({
                    'success': False,
                    'error': 'Error al crear consulta'
                }), 500
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def update_consulta(self, consulta_id):
        """Actualiza una consulta existente"""
        try:
            data = request.get_json()
            consulta = self.consulta_service.update_consulta(consulta_id, data)
            if consulta:
                return jsonify({
                    'success': True,
                    'data': consulta,
                    'message': 'Consulta actualizada exitosamente'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Consulta no encontrada'
                }), 404
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def delete_consulta(self, consulta_id):
        """Elimina una consulta"""
        try:
            success = self.consulta_service.delete_consulta(consulta_id)
            if success:
                return jsonify({
                    'success': True,
                    'message': 'Consulta eliminada exitosamente'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Consulta no encontrada'
                }), 404
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def get_consultas_hoy(self):
        """Obtiene las consultas de hoy"""
        try:
            consultas = self.consulta_service.get_consultas_hoy()
            return jsonify({
                'success': True,
                'data': consultas,
                'total': len(consultas)
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def get_diagnosticos(self):
        """Obtiene todos los diagnósticos disponibles"""
        try:
            query = request.args.get('q', '')
            if query:
                diagnosticos = self.consulta_service.search_diagnosticos(query)
            else:
                diagnosticos = self.consulta_service.get_diagnosticos_disponibles()
            
            return jsonify({
                'success': True,
                'data': diagnosticos,
                'total': len(diagnosticos)
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500"# ARCHIVO MOVIDO A archivos_en_deshuso/consulta_medica_controller.py"
'''