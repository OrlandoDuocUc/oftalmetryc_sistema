from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from app.infraestructure.repositories.proveedor_repository import ProveedorRepository
from app.domain.models.proveedor import Proveedor
from app.infraestructure.utils.db_session import get_db_session
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProveedorController:
    """
    Controlador para gestión de proveedores
    """
    
    def __init__(self):
        self.db_session = get_db_session()
        self.repository = ProveedorRepository(self.db_session)
    
    def listar_proveedores(self):
        """Página principal de proveedores"""
        try:
            # Verificar sesión
            if 'user_id' not in session:
                return redirect(url_for('login'))
            
            # Obtener parámetros de búsqueda
            search_term = request.args.get('search', '')
            
            if search_term:
                proveedores = self.repository.search(search_term)
            else:
                proveedores = self.repository.get_all()
            
            # Obtener estadísticas
            stats = self.repository.get_statistics()
            
            return render_template('proveedores.html', 
                                   proveedores=proveedores,
                                   stats=stats,
                                   search_term=search_term)
        except Exception as e:
            logger.error(f"Error al listar proveedores: {e}")
            return render_template('proveedores.html', 
                                   proveedores=[],
                                   stats={},
                                   error="Error al cargar los proveedores")
    
    def crear_proveedor(self):
        """Crear nuevo proveedor"""
        try:
            if request.method == 'GET':
                return render_template('crear_proveedor.html')
            
            # Verificar sesión
            if 'user_id' not in session:
                return jsonify({'success': False, 'message': 'Sesión no válida'}), 401
            
            data = request.get_json()
            
            # Validaciones básicas
            if not data.get('razon_social'):
                return jsonify({'success': False, 'message': 'La razón social es obligatoria'}), 400
            
            if not data.get('rut'):
                return jsonify({'success': False, 'message': 'El RUT es obligatorio'}), 400
            
            # Verificar si ya existe proveedor con el mismo RUT
            proveedor_existe = self.repository.get_by_rut(data.get('rut'))
            if proveedor_existe:
                return jsonify({'success': False, 'message': 'Ya existe un proveedor con este RUT'}), 400
            
            # Crear nuevo proveedor
            proveedor = Proveedor(
                razon_social=data.get('razon_social'),
                nombre_comercial=data.get('nombre_comercial'),
                rut=data.get('rut'),
                direccion=data.get('direccion'),
                telefono=data.get('telefono'),
                email=data.get('email'),
                sitio_web=data.get('sitio_web'),
                categoria_productos=data.get('categoria_productos'),
                condiciones_pago=data.get('condiciones_pago', 'Contado'),
                plazo_pago_dias=data.get('plazo_pago_dias', 0),
                descuento_volumen=data.get('descuento_volumen', 0.0),
                representante_nombre=data.get('representante_nombre'),
                representante_telefono=data.get('representante_telefono'),
                representante_email=data.get('representante_email'),
                observaciones=data.get('observaciones')
            )
            
            success = self.repository.save(proveedor)
            
            if success:
                return jsonify({
                    'success': True, 
                    'message': 'Proveedor creado exitosamente',
                    'proveedor_id': proveedor.proveedor_id
                })
            else:
                return jsonify({'success': False, 'message': 'Error al crear el proveedor'}), 500
                
        except Exception as e:
            logger.error(f"Error al crear proveedor: {e}")
            return jsonify({'success': False, 'message': f'Error interno: {str(e)}'}), 500
    
    def editar_proveedor(self, proveedor_id):
        """Editar proveedor existente"""
        try:
            if request.method == 'GET':
                proveedor = self.repository.get_by_id(proveedor_id)
                if not proveedor:
                    return render_template('error.html', message='Proveedor no encontrado'), 404
                return render_template('editar_proveedor.html', proveedor=proveedor)
            
            # Verificar sesión
            if 'user_id' not in session:
                return jsonify({'success': False, 'message': 'Sesión no válida'}), 401
            
            data = request.get_json()
            
            # Obtener proveedor existente
            proveedor = self.repository.get_by_id(proveedor_id)
            if not proveedor:
                return jsonify({'success': False, 'message': 'Proveedor no encontrado'}), 404
            
            # Validaciones básicas
            if not data.get('razon_social'):
                return jsonify({'success': False, 'message': 'La razón social es obligatoria'}), 400
            
            if not data.get('rut'):
                return jsonify({'success': False, 'message': 'El RUT es obligatorio'}), 400
            
            # Verificar si existe otro proveedor con el mismo RUT
            proveedor_rut = self.repository.get_by_rut(data.get('rut'))
            if proveedor_rut and proveedor_rut.proveedor_id != proveedor_id:
                return jsonify({'success': False, 'message': 'Ya existe otro proveedor con este RUT'}), 400
            
            # Actualizar datos
            proveedor.razon_social = data.get('razon_social')
            proveedor.nombre_comercial = data.get('nombre_comercial')
            proveedor.rut = data.get('rut')
            proveedor.direccion = data.get('direccion')
            proveedor.telefono = data.get('telefono')
            proveedor.email = data.get('email')
            proveedor.sitio_web = data.get('sitio_web')
            proveedor.categoria_productos = data.get('categoria_productos')
            proveedor.condiciones_pago = data.get('condiciones_pago', 'Contado')
            proveedor.plazo_pago_dias = data.get('plazo_pago_dias', 0)
            proveedor.descuento_volumen = data.get('descuento_volumen', 0.0)
            proveedor.representante_nombre = data.get('representante_nombre')
            proveedor.representante_telefono = data.get('representante_telefono')
            proveedor.representante_email = data.get('representante_email')
            proveedor.observaciones = data.get('observaciones')
            
            success = self.repository.update(proveedor)
            
            if success:
                return jsonify({
                    'success': True, 
                    'message': 'Proveedor actualizado exitosamente'
                })
            else:
                return jsonify({'success': False, 'message': 'Error al actualizar el proveedor'}), 500
                
        except Exception as e:
            logger.error(f"Error al editar proveedor: {e}")
            return jsonify({'success': False, 'message': f'Error interno: {str(e)}'}), 500
    
    def ver_proveedor(self, proveedor_id):
        """Ver detalles de un proveedor"""
        try:
            proveedor = self.repository.get_by_id(proveedor_id)
            if not proveedor:
                return render_template('error.html', message='Proveedor no encontrado'), 404
            
            return render_template('detalle_proveedor.html', proveedor=proveedor)
            
        except Exception as e:
            logger.error(f"Error al ver proveedor: {e}")
            return render_template('error.html', message='Error al cargar el proveedor'), 500
    
    def eliminar_proveedor(self, proveedor_id):
        """Eliminar (desactivar) proveedor"""
        try:
            # Verificar sesión
            if 'user_id' not in session:
                return jsonify({'success': False, 'message': 'Sesión no válida'}), 401
            
            success = self.repository.delete(proveedor_id)
            
            if success:
                return jsonify({
                    'success': True, 
                    'message': 'Proveedor eliminado exitosamente'
                })
            else:
                return jsonify({'success': False, 'message': 'Error al eliminar el proveedor'}), 500
                
        except Exception as e:
            logger.error(f"Error al eliminar proveedor: {e}")
            return jsonify({'success': False, 'message': f'Error interno: {str(e)}'}), 500
    
    def buscar_proveedores(self):
        """API para buscar proveedores"""
        try:
            term = request.args.get('term', '')
            proveedores = self.repository.search(term)
            
            result = []
            for p in proveedores:
                result.append({
                    'id': p.proveedor_id,
                    'codigo': p.codigo_proveedor,
                    'razon_social': p.razon_social,
                    'nombre_comercial': p.nombre_comercial,
                    'rut': p.rut,
                    'email': p.email,
                    'telefono': p.telefono
                })
            
            return jsonify({'success': True, 'proveedores': result})
            
        except Exception as e:
            logger.error(f"Error al buscar proveedores: {e}")
            return jsonify({'success': False, 'message': 'Error en la búsqueda'}), 500
    
    def obtener_proveedor_api(self, proveedor_id):
        """API para obtener datos de un proveedor"""
        try:
            proveedor = self.repository.get_by_id(proveedor_id)
            if not proveedor:
                return jsonify({'success': False, 'message': 'Proveedor no encontrado'}), 404
            
            data = {
                'proveedor_id': proveedor.proveedor_id,
                'codigo_proveedor': proveedor.codigo_proveedor,
                'razon_social': proveedor.razon_social,
                'nombre_comercial': proveedor.nombre_comercial,
                'rut': proveedor.rut,
                'direccion': proveedor.direccion,
                'telefono': proveedor.telefono,
                'email': proveedor.email,
                'sitio_web': proveedor.sitio_web,
                'categoria_productos': proveedor.categoria_productos,
                'condiciones_pago': proveedor.condiciones_pago,
                'plazo_pago_dias': proveedor.plazo_pago_dias,
                'descuento_volumen': float(proveedor.descuento_volumen) if proveedor.descuento_volumen is not None else 0.0,
                'representante_nombre': proveedor.representante_nombre,
                'representante_telefono': proveedor.representante_telefono,
                'representante_email': proveedor.representante_email,
                'observaciones': proveedor.observaciones,
                'fecha_registro': proveedor.fecha_registro.isoformat() if proveedor.fecha_registro else None,
                'estado': proveedor.estado
            }
            
            return jsonify({'success': True, 'proveedor': data})
            
        except Exception as e:
            logger.error(f"Error al obtener proveedor: {e}")
            return jsonify({'success': False, 'message': 'Error al obtener el proveedor'}), 500
    
    def __del__(self):
        """Cerrar sesión de base de datos"""
        if hasattr(self, 'db_session'):
            self.db_session.close()