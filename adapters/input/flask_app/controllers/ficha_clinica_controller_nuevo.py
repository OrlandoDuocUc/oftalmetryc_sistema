from flask import request, jsonify
from app.infraestructure.utils.db import SessionLocal
from app.domain.models.consulta_medica import FichaClinica
from app.domain.models.paciente import PacienteMedico
from app.domain.models.user import User
from sqlalchemy.orm import joinedload
from datetime import datetime

class FichaClinicaController:
    """
    Controlador para gestionar fichas clínicas según estructura SQL real
    """
    
    def __init__(self):
        pass
    
    def get_all_fichas_clinicas(self):
        """Obtiene todas las fichas clínicas"""
        try:
            session = SessionLocal()
            try:
                fichas = session.query(FichaClinica)\
                    .options(
                        joinedload(FichaClinica.paciente_medico),
                        joinedload(FichaClinica.usuario)
                    )\
                    .order_by(FichaClinica.fecha_consulta.desc())\
                    .all()
                
                result = []
                for ficha in fichas:
                    data = ficha.to_dict()
                    
                    # Agregar información del paciente médico
                    if ficha.paciente_medico:
                        data['paciente_medico'] = {
                            'paciente_medico_id': ficha.paciente_medico.paciente_medico_id,
                            'numero_ficha': ficha.paciente_medico.numero_ficha
                        }
                        
                        # Agregar información del cliente si existe
                        if ficha.paciente_medico.cliente:
                            data['cliente'] = {
                                'nombres': ficha.paciente_medico.cliente.nombres,
                                'ap_pat': ficha.paciente_medico.cliente.ap_pat,
                                'ap_mat': ficha.paciente_medico.cliente.ap_mat,
                                'rut': ficha.paciente_medico.cliente.rut
                            }
                    
                    # Agregar información del usuario
                    if ficha.usuario:
                        data['usuario'] = {
                            'usuario_id': ficha.usuario.usuario_id,
                            'nombre': ficha.usuario.nombre,
                            'username': ficha.usuario.username
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
    
    def get_ficha_clinica_by_id(self, ficha_id):
        """Obtiene una ficha clínica por ID"""
        try:
            session = SessionLocal()
            try:
                ficha = session.query(FichaClinica)\
                    .options(
                        joinedload(FichaClinica.paciente_medico),
                        joinedload(FichaClinica.usuario)
                    )\
                    .filter(FichaClinica.ficha_id == ficha_id)\
                    .first()
                
                if ficha:
                    data = ficha.to_dict()
                    
                    if ficha.paciente_medico:
                        data['paciente_medico'] = ficha.paciente_medico.to_dict()
                        if ficha.paciente_medico.cliente:
                            data['cliente'] = {
                                'nombres': ficha.paciente_medico.cliente.nombres,
                                'ap_pat': ficha.paciente_medico.cliente.ap_pat,
                                'ap_mat': ficha.paciente_medico.cliente.ap_mat,
                                'rut': ficha.paciente_medico.cliente.rut
                            }
                    
                    if ficha.usuario:
                        data['usuario'] = {
                            'nombre': ficha.usuario.nombre,
                            'username': ficha.usuario.username
                        }
                    
                    return jsonify({
                        'success': True,
                        'data': data
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Ficha clínica no encontrada'
                    }), 404
            finally:
                session.close()
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def create_ficha_clinica(self):
        """Crea una nueva ficha clínica"""
        try:
            data = request.get_json()
            session = SessionLocal()
            try:
                # Validaciones básicas
                if not data.get('paciente_medico_id'):
                    return jsonify({
                        'success': False,
                        'error': 'ID del paciente médico es obligatorio'
                    }), 400
                
                if not data.get('numero_consulta'):
                    return jsonify({
                        'success': False,
                        'error': 'Número de consulta es obligatorio'
                    }), 400
                
                # Crear nueva ficha clínica
                nueva_ficha = FichaClinica(
                    paciente_medico_id=data.get('paciente_medico_id'),
                    usuario_id=data.get('usuario_id', 1),  # Default admin user
                    numero_consulta=data.get('numero_consulta'),
                    fecha_consulta=datetime.fromisoformat(data.get('fecha_consulta').replace('Z', '+00:00')) if data.get('fecha_consulta') else datetime.now(),
                    motivo_consulta=data.get('motivo_consulta'),
                    historia_actual=data.get('historia_actual'),
                    
                    # Agudeza Visual
                    av_od_sc=data.get('av_od_sc'),
                    av_od_cc=data.get('av_od_cc'),
                    av_od_ph=data.get('av_od_ph'),
                    av_od_cerca=data.get('av_od_cerca'),
                    av_oi_sc=data.get('av_oi_sc'),
                    av_oi_cc=data.get('av_oi_cc'),
                    av_oi_ph=data.get('av_oi_ph'),
                    av_oi_cerca=data.get('av_oi_cerca'),
                    
                    # Refracción
                    esfera_od=data.get('esfera_od'),
                    cilindro_od=data.get('cilindro_od'),
                    eje_od=data.get('eje_od'),
                    adicion_od=data.get('adicion_od'),
                    esfera_oi=data.get('esfera_oi'),
                    cilindro_oi=data.get('cilindro_oi'),
                    eje_oi=data.get('eje_oi'),
                    adicion_oi=data.get('adicion_oi'),
                    
                    # Datos generales
                    distancia_pupilar=data.get('distancia_pupilar'),
                    tipo_lente=data.get('tipo_lente'),
                    estado=data.get('estado', 'en_proceso')
                )
                
                session.add(nueva_ficha)
                session.commit()
                session.refresh(nueva_ficha)
                
                return jsonify({
                    'success': True,
                    'data': nueva_ficha.to_dict(),
                    'message': 'Ficha clínica creada exitosamente'
                }), 201
            finally:
                session.close()
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def update_ficha_clinica(self, ficha_id):
        """Actualiza una ficha clínica existente"""
        try:
            data = request.get_json()
            session = SessionLocal()
            try:
                ficha = session.query(FichaClinica)\
                    .filter(FichaClinica.ficha_id == ficha_id)\
                    .first()
                
                if not ficha:
                    return jsonify({
                        'success': False,
                        'error': 'Ficha clínica no encontrada'
                    }), 404
                
                # Actualizar campos
                for key, value in data.items():
                    if hasattr(ficha, key) and key != 'ficha_id':
                        setattr(ficha, key, value)
                
                session.commit()
                session.refresh(ficha)
                
                return jsonify({
                    'success': True,
                    'data': ficha.to_dict(),
                    'message': 'Ficha clínica actualizada exitosamente'
                })
            finally:
                session.close()
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def get_consultas_by_paciente(self, paciente_medico_id):
        """Obtiene todas las consultas/fichas clínicas de un paciente específico"""
        try:
            session = SessionLocal()
            try:
                fichas = session.query(FichaClinica)\
                    .options(
                        joinedload(FichaClinica.paciente_medico),
                        joinedload(FichaClinica.usuario)
                    )\
                    .filter(FichaClinica.paciente_medico_id == paciente_medico_id)\
                    .order_by(FichaClinica.fecha_consulta.desc())\
                    .all()
                
                result = []
                for ficha in fichas:
                    data = ficha.to_dict()
                    
                    # Agregar información del paciente médico
                    if ficha.paciente_medico:
                        data['paciente_medico'] = {
                            'paciente_medico_id': ficha.paciente_medico.paciente_medico_id,
                            'numero_ficha': ficha.paciente_medico.numero_ficha
                        }
                        
                        # Agregar información del cliente si existe
                        if ficha.paciente_medico.cliente:
                            data['cliente'] = {
                                'nombres': ficha.paciente_medico.cliente.nombres,
                                'ap_pat': ficha.paciente_medico.cliente.ap_pat,
                                'ap_mat': ficha.paciente_medico.cliente.ap_mat,
                                'rut': ficha.paciente_medico.cliente.rut
                            }
                    
                    # Agregar información del usuario
                    if ficha.usuario:
                        data['usuario'] = {
                            'usuario_id': ficha.usuario.usuario_id,
                            'nombre': ficha.usuario.nombre
                        }
                    
                    result.append(data)
                
                return jsonify({
                    'success': True,
                    'consultas': result,
                    'total': len(result)
                })
            finally:
                session.close()
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    def get_ficha_clinica_by_id(self, ficha_id):
        """Obtiene una ficha clínica específica por ID"""
        try:
            session = SessionLocal()
            try:
                ficha = session.query(FichaClinica)\
                    .options(
                        joinedload(FichaClinica.paciente_medico),
                        joinedload(FichaClinica.usuario)
                    )\
                    .filter(FichaClinica.ficha_id == ficha_id)\
                    .first()
                
                if not ficha:
                    return jsonify({
                        'success': False,
                        'message': 'Ficha clínica no encontrada'
                    }), 404
                
                data = ficha.to_dict()
                
                # Agregar información del paciente médico
                if ficha.paciente_medico:
                    data['paciente_medico'] = {
                        'paciente_medico_id': ficha.paciente_medico.paciente_medico_id,
                        'numero_ficha': ficha.paciente_medico.numero_ficha
                    }
                    
                    # Agregar información del cliente si existe
                    if ficha.paciente_medico.cliente:
                        data['cliente'] = {
                            'nombres': ficha.paciente_medico.cliente.nombres,
                            'ap_pat': ficha.paciente_medico.cliente.ap_pat,
                            'ap_mat': ficha.paciente_medico.cliente.ap_mat,
                            'rut': ficha.paciente_medico.cliente.rut
                        }
                
                # Agregar información del usuario
                if ficha.usuario:
                    data['usuario'] = {
                        'usuario_id': ficha.usuario.usuario_id,
                        'nombre': ficha.usuario.nombre
                    }
                
                return jsonify({
                    'success': True,
                    'ficha_clinica': data
                })
            finally:
                session.close()
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500