from flask import jsonify, request
from app.infraestructure.utils.db import SessionLocal
from app.domain.models.paciente import PacienteMedico
from app.domain.models.cliente import Cliente
from sqlalchemy.orm import joinedload

class PacienteMedicoController:
    def __init__(self):
        pass
    
    def get_all_pacientes_medicos(self):
        """Obtiene todos los pacientes médicos con información del cliente"""
        try:
            session = SessionLocal()
            try:
                pacientes_medicos = session.query(PacienteMedico)\
                    .options(joinedload(PacienteMedico.cliente))\
                    .filter(PacienteMedico.estado == True)\
                    .all()
                
                result = []
                for pm in pacientes_medicos:
                    data = pm.to_dict()
                    if pm.cliente:
                        data['cliente'] = {
                            'cliente_id': pm.cliente.cliente_id,
                            'nombres': pm.cliente.nombres,
                            'ap_pat': pm.cliente.ap_pat,
                            'ap_mat': pm.cliente.ap_mat,
                            'rut': pm.cliente.rut,
                            'email': pm.cliente.email,
                            'telefono': pm.cliente.telefono,
                            'fecha_nacimiento': pm.cliente.fecha_nacimiento.isoformat() if pm.cliente.fecha_nacimiento else None
                        }
                    result.append(data)
                
                return jsonify({
                    'success': True,
                    'data': result,
                    'total': len(result)
                })
            finally:
                session.close()
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def get_paciente_medico_by_id(self, paciente_medico_id):
        """Obtiene un paciente médico por ID"""
        try:
            session = SessionLocal()
            try:
                paciente_medico = session.query(PacienteMedico)\
                    .options(joinedload(PacienteMedico.cliente))\
                    .filter(PacienteMedico.paciente_medico_id == paciente_medico_id)\
                    .first()
                
                if paciente_medico:
                    data = paciente_medico.to_dict()
                    if paciente_medico.cliente:
                        data['cliente'] = {
                            'cliente_id': paciente_medico.cliente.cliente_id,
                            'nombres': paciente_medico.cliente.nombres,
                            'ap_pat': paciente_medico.cliente.ap_pat,
                            'ap_mat': paciente_medico.cliente.ap_mat,
                            'rut': paciente_medico.cliente.rut,
                            'email': paciente_medico.cliente.email,
                            'telefono': paciente_medico.cliente.telefono,
                            'direccion': paciente_medico.cliente.direccion,
                            'fecha_nacimiento': paciente_medico.cliente.fecha_nacimiento.isoformat() if paciente_medico.cliente.fecha_nacimiento else None
                        }
                    
                    return jsonify({
                        'success': True,
                        'data': data
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Paciente médico no encontrado'
                    }), 404
            finally:
                session.close()
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def search_pacientes_medicos(self):
        """Busca pacientes médicos"""
        try:
            query = request.args.get('q', '')
            session = SessionLocal()
            try:
                pacientes_medicos = session.query(PacienteMedico)\
                    .options(joinedload(PacienteMedico.cliente))\
                    .join(Cliente, PacienteMedico.cliente_id == Cliente.cliente_id)\
                    .filter(
                        (Cliente.nombres.ilike(f'%{query}%')) |
                        (Cliente.ap_pat.ilike(f'%{query}%')) |
                        (Cliente.rut.ilike(f'%{query}%')) |
                        (PacienteMedico.numero_ficha.ilike(f'%{query}%'))
                    )\
                    .filter(PacienteMedico.estado == True)\
                    .all()
                
                result = []
                for pm in pacientes_medicos:
                    data = pm.to_dict()
                    if pm.cliente:
                        data['cliente'] = {
                            'nombres': pm.cliente.nombres,
                            'ap_pat': pm.cliente.ap_pat,
                            'ap_mat': pm.cliente.ap_mat,
                            'rut': pm.cliente.rut
                        }
                    result.append(data)
                
                return jsonify({
                    'success': True,
                    'data': result,
                    'total': len(result)
                })
            finally:
                session.close()
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def create_paciente_medico(self):
        """Crea un nuevo paciente médico"""
        try:
            data = request.get_json()
            session = SessionLocal()
            try:
                # Verificar que los datos tengan la estructura esperada
                if 'cliente' not in data or 'paciente_medico' not in data:
                    return jsonify({
                        'success': False,
                        'error': 'Estructura de datos incorrecta. Se esperan objetos "cliente" y "paciente_medico"'
                    }), 400
                
                cliente_data = data['cliente']
                paciente_data = data['paciente_medico']
                
                # 1. Crear el cliente primero
                nuevo_cliente = Cliente(
                    nombres=cliente_data.get('nombres'),
                    ap_pat=cliente_data.get('ap_pat'),
                    ap_mat=cliente_data.get('ap_mat'),
                    rut=cliente_data.get('rut'),
                    email=cliente_data.get('email'),
                    telefono=cliente_data.get('telefono'),
                    direccion=cliente_data.get('direccion'),
                    fecha_nacimiento=cliente_data.get('fecha_nacimiento'),
                    estado=True
                )
                
                session.add(nuevo_cliente)
                session.flush()  # Para obtener el ID sin hacer commit
                
                # 2. Generar número de ficha automáticamente
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                numero_ficha = f"FM-{timestamp}"
                
                # 3. Crear el paciente médico con el cliente_id
                nuevo_paciente = PacienteMedico(
                    cliente_id=nuevo_cliente.cliente_id,
                    numero_ficha=numero_ficha,
                    antecedentes_medicos=paciente_data.get('antecedentes_medicos'),
                    antecedentes_oculares=paciente_data.get('antecedentes_oculares'),
                    alergias=paciente_data.get('alergias'),
                    medicamentos_actuales=paciente_data.get('medicamentos_actuales'),
                    contacto_emergencia=paciente_data.get('contacto_emergencia'),
                    telefono_emergencia=paciente_data.get('telefono_emergencia'),
                    estado=True
                )
                
                session.add(nuevo_paciente)
                session.commit()
                session.refresh(nuevo_paciente)
                session.refresh(nuevo_cliente)
                
                # Preparar datos de respuesta
                response_data = nuevo_paciente.to_dict()
                response_data['cliente'] = {
                    'nombres': nuevo_cliente.nombres,
                    'ap_pat': nuevo_cliente.ap_pat,
                    'ap_mat': nuevo_cliente.ap_mat,
                    'rut': nuevo_cliente.rut,
                    'email': nuevo_cliente.email,
                    'telefono': nuevo_cliente.telefono,
                    'direccion': nuevo_cliente.direccion,
                    'fecha_nacimiento': nuevo_cliente.fecha_nacimiento.isoformat() if nuevo_cliente.fecha_nacimiento else None
                }
                
                return jsonify({
                    'success': True,
                    'data': response_data,
                    'message': 'Paciente médico creado exitosamente'
                }), 201
            except Exception as e:
                session.rollback()
                raise e
            finally:
                session.close()
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
    
    def update_paciente_medico(self, paciente_medico_id):
        """Actualiza un paciente médico y su cliente asociado"""
        try:
            session = SessionLocal()
            try:
                # Obtener datos del request
                data = request.json
                cliente_data = data.get('cliente', {})
                paciente_data = data.get('paciente_medico', {})
                
                # Buscar el paciente médico
                paciente_medico = session.query(PacienteMedico)\
                    .options(joinedload(PacienteMedico.cliente))\
                    .filter(PacienteMedico.paciente_medico_id == paciente_medico_id)\
                    .first()
                
                if not paciente_medico:
                    return jsonify({
                        'success': False,
                        'error': 'Paciente médico no encontrado'
                    }), 404
                
                # Actualizar cliente si existe
                if paciente_medico.cliente and cliente_data:
                    cliente = paciente_medico.cliente
                    
                    # Actualizar campos del cliente
                    if 'nombres' in cliente_data:
                        cliente.nombres = cliente_data['nombres']
                    if 'apellido_paterno' in cliente_data:
                        cliente.apellido_paterno = cliente_data['apellido_paterno']
                    if 'apellido_materno' in cliente_data:
                        cliente.apellido_materno = cliente_data['apellido_materno']
                    if 'rut' in cliente_data:
                        cliente.rut = cliente_data['rut']
                    if 'email' in cliente_data:
                        cliente.email = cliente_data['email']
                    if 'telefono' in cliente_data:
                        cliente.telefono = cliente_data['telefono']
                    if 'direccion' in cliente_data:
                        cliente.direccion = cliente_data['direccion']
                    if 'fecha_nacimiento' in cliente_data and cliente_data['fecha_nacimiento']:
                        from datetime import datetime
                        cliente.fecha_nacimiento = datetime.strptime(cliente_data['fecha_nacimiento'], '%Y-%m-%d').date()
                
                # Actualizar paciente médico
                if paciente_data:
                    if 'antecedentes_medicos' in paciente_data:
                        paciente_medico.antecedentes_medicos = paciente_data['antecedentes_medicos']
                    if 'antecedentes_oculares' in paciente_data:
                        paciente_medico.antecedentes_oculares = paciente_data['antecedentes_oculares']
                    if 'alergias' in paciente_data:
                        paciente_medico.alergias = paciente_data['alergias']
                    if 'medicamentos_actuales' in paciente_data:
                        paciente_medico.medicamentos_actuales = paciente_data['medicamentos_actuales']
                    if 'contacto_emergencia' in paciente_data:
                        paciente_medico.contacto_emergencia = paciente_data['contacto_emergencia']
                    if 'telefono_emergencia' in paciente_data:
                        paciente_medico.telefono_emergencia = paciente_data['telefono_emergencia']
                    if 'estado' in paciente_data:
                        paciente_medico.estado = paciente_data['estado']
                
                # Guardar cambios
                session.commit()
                
                return jsonify({
                    'success': True,
                    'message': 'Paciente actualizado exitosamente'
                })
                
            finally:
                session.close()
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500