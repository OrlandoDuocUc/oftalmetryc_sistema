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
    
    @staticmethod
    def buscar_pacientes():
        """
        Búsqueda de pacientes via AJAX
        """
        try:
            termino = request.args.get('q', '').strip()
            
            if len(termino) < 2:
                return jsonify({
                    'success': False,
                    'message': 'El término de búsqueda debe tener al menos 2 caracteres'
                })
            
            with get_db_session() as db_session:
                service = FichaClinicaService(db_session)
                resultados = service.buscar_pacientes_avanzado(termino)
                
                # Formatear resultados para JSON
                pacientes_json = []
                for resultado in resultados:
                    paciente = resultado['paciente']
                    pacientes_json.append({
                        'id': paciente.id,
                        'ci': paciente.ci,
                        'nombre_completo': paciente.nombre_completo,
                        'telefono': paciente.telefono,
                        'edad': paciente.edad,
                        'ultima_consulta': resultado['ultima_consulta'].isoformat() if resultado['ultima_consulta'] else None,
                        'total_consultas': resultado['total_consultas']
                    })
                
                return jsonify({
                    'success': True,
                    'pacientes': pacientes_json
                })
                
        except Exception as e:
            logger.error(f"Error en buscar_pacientes: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Error en la búsqueda de pacientes'
            })
    
    @staticmethod
    def perfil_paciente(paciente_id: int):
        """
        Muestra el perfil completo del paciente
        """
        try:
            with get_db_session() as db_session:
                service = FichaClinicaService(db_session)
                perfil = service.obtener_perfil_completo_paciente(paciente_id)
                
                if not perfil:
                    flash('Paciente no encontrado', 'error')
                    return redirect(url_for('ficha_clinica.index'))
                
                return render_template('ficha_clinica/perfil_paciente.html', 
                                     perfil=perfil)
                
        except Exception as e:
            logger.error(f"Error en perfil_paciente: {str(e)}")
            flash('Error al cargar el perfil del paciente', 'error')
            return redirect(url_for('ficha_clinica.index'))
    
    @staticmethod
    def crear_paciente():
        """
        Formulario para crear nuevo paciente
        """
        if request.method == 'GET':
            return render_template('ficha_clinica/crear_paciente.html')
        
        try:
            # Obtener datos del formulario
            datos_paciente = {
                'ci': request.form.get('ci', '').strip(),
                'nombres': request.form.get('nombres', '').strip(),
                'apellidos': request.form.get('apellidos', '').strip(),
                'telefono': request.form.get('telefono', '').strip(),
                'email': request.form.get('email', '').strip(),
                'direccion': request.form.get('direccion', '').strip(),
                'fecha_nacimiento': datetime.strptime(request.form.get('fecha_nacimiento'), '%Y-%m-%d').date() if request.form.get('fecha_nacimiento') else None,
                'genero': request.form.get('genero', ''),
                'ocupacion': request.form.get('ocupacion', '').strip(),
                'hobby': request.form.get('hobby', '').strip(),
                'observaciones_generales': request.form.get('observaciones_generales', '').strip()
            }
            
            with get_db_session() as db_session:
                service = FichaClinicaService(db_session)
                
                # Validar cédula
                valida, mensaje = service.validar_cedula_ecuador(datos_paciente['ci'])
                if not valida:
                    flash(f'Cédula inválida: {mensaje}', 'error')
                    return render_template('ficha_clinica/crear_paciente.html', datos=datos_paciente)
                
                # Verificar si ya existe
                paciente_existente = service.paciente_repo.obtener_por_ci(datos_paciente['ci'])
                if paciente_existente:
                    flash('Ya existe un paciente con esta cédula', 'warning')
                    return redirect(url_for('ficha_clinica.perfil_paciente', paciente_id=paciente_existente.id))
                
                # Crear paciente
                paciente = service.paciente_repo.crear_paciente(datos_paciente)
                flash(f'Paciente {paciente.nombre_completo} creado exitosamente', 'success')
                
                return redirect(url_for('ficha_clinica.perfil_paciente', paciente_id=paciente.id))
                
        except Exception as e:
            logger.error(f"Error en crear_paciente: {str(e)}")
            flash('Error al crear el paciente', 'error')
            return render_template('ficha_clinica/crear_paciente.html', datos=request.form)
    
    @staticmethod
    def crear_ficha(paciente_id: int):
        """
        Formulario para crear nueva ficha clínica
        """
        try:
            with get_db_session() as db_session:
                service = FichaClinicaService(db_session)
                paciente = service.paciente_repo.obtener_por_id(paciente_id)
                
                if not paciente:
                    flash('Paciente no encontrado', 'error')
                    return redirect(url_for('ficha_clinica.index'))
                
                if request.method == 'GET':
                    # Obtener última ficha para pre-llenar algunos campos
                    ultima_ficha = service.ficha_repo.obtener_ultima_ficha_paciente(paciente_id)
                    
                    return render_template('ficha_clinica/crear_ficha.html', 
                                         paciente=paciente,
                                         ultima_ficha=ultima_ficha)
                
                # POST: Procesar formulario
                return FichaClinicaController._procesar_formulario_ficha(service, paciente_id)
                
        except Exception as e:
            logger.error(f"Error en crear_ficha: {str(e)}")
            flash('Error al crear la ficha clínica', 'error')
            return redirect(url_for('ficha_clinica.perfil_paciente', paciente_id=paciente_id))
    
    @staticmethod
    def editar_ficha(ficha_id: int):
        """
        Formulario para editar ficha clínica existente
        """
        try:
            with get_db_session() as db_session:
                service = FichaClinicaService(db_session)
                datos_completos = service.obtener_ficha_completa(ficha_id)
                
                if not datos_completos:
                    flash('Ficha clínica no encontrada', 'error')
                    return redirect(url_for('ficha_clinica.index'))
                
                if request.method == 'GET':
                    return render_template('ficha_clinica/editar_ficha.html', 
                                         datos=datos_completos)
                
                # POST: Procesar actualización
                return FichaClinicaController._procesar_formulario_ficha(
                    service, datos_completos['paciente'].id, ficha_id)
                
        except Exception as e:
            logger.error(f"Error en editar_ficha: {str(e)}")
            flash('Error al editar la ficha clínica', 'error')
            return redirect(url_for('ficha_clinica.index'))
    
    @staticmethod
    def ver_ficha(ficha_id: int):
        """
        Visualizar ficha clínica completa
        """
        try:
            with get_db_session() as db_session:
                service = FichaClinicaService(db_session)
                datos_completos = service.obtener_ficha_completa(ficha_id)
                
                if not datos_completos:
                    flash('Ficha clínica no encontrada', 'error')
                    return redirect(url_for('ficha_clinica.index'))
                
                return render_template('ficha_clinica/ver_ficha.html', 
                                     datos=datos_completos)
                
        except Exception as e:
            logger.error(f"Error en ver_ficha: {str(e)}")
            flash('Error al visualizar la ficha clínica', 'error')
            return redirect(url_for('ficha_clinica.index'))
    
    @staticmethod
    def imprimir_ficha(ficha_id: int):
        """
        Versión para impresión de la ficha clínica
        """
        try:
            with get_db_session() as db_session:
                service = FichaClinicaService(db_session)
                resumen = service.generar_resumen_ficha(ficha_id)
                
                if not resumen:
                    flash('Ficha clínica no encontrada', 'error')
                    return redirect(url_for('ficha_clinica.index'))
                
                return render_template('ficha_clinica/imprimir_ficha.html', 
                                     resumen=resumen)
                
        except Exception as e:
            logger.error(f"Error en imprimir_ficha: {str(e)}")
            flash('Error al generar la ficha para impresión', 'error')
            return redirect(url_for('ficha_clinica.index'))
    
    @staticmethod
    def historial_paciente(paciente_id: int):
        """
        Historial completo de consultas del paciente
        """
        try:
            with get_db_session() as db_session:
                service = FichaClinicaService(db_session)
                historial = service.obtener_historial_paciente(paciente_id)
                
                return render_template('ficha_clinica/historial_paciente.html', 
                                     historial=historial)
                
        except Exception as e:
            logger.error(f"Error en historial_paciente: {str(e)}")
            flash('Error al cargar el historial del paciente', 'error')
            return redirect(url_for('ficha_clinica.index'))
    
    # =========================================================================
    # MÉTODOS AUXILIARES
    # =========================================================================
    
    @staticmethod
    def _procesar_formulario_ficha(service: FichaClinicaService, paciente_id: int, ficha_id: int = None) -> Any:
        """
        Procesa el formulario de ficha clínica (crear o editar)
        """
        try:
            # Datos de la ficha clínica
            datos_ficha = {
                'motivo_consulta': request.form.get('motivo_consulta', '').strip(),
                'ultimo_control_visual': datetime.strptime(request.form.get('ultimo_control_visual'), '%Y-%m-%d').date() if request.form.get('ultimo_control_visual') else None,
                'usa_lentes': request.form.get('usa_lentes') == 'on',
                'ultimo_cambio_lentes': datetime.strptime(request.form.get('ultimo_cambio_lentes'), '%Y-%m-%d').date() if request.form.get('ultimo_cambio_lentes') else None,
                'antecedentes_personales': request.form.get('antecedentes_personales', '').strip(),
                'antecedentes_familiares': request.form.get('antecedentes_familiares', '').strip(),
                'diagnostico_general': request.form.get('diagnostico_general', '').strip(),
                'tratamiento_general': request.form.get('tratamiento_general', '').strip(),
                'firma_responsable': request.form.get('firma_responsable', '').strip(),
                'conforme_evaluado': request.form.get('conforme_evaluado') == 'on'
            }
            
            # Datos del examen oftalmológico (todos los campos)
            datos_examen = FichaClinicaController._extraer_datos_examen(request.form)
            
            if ficha_id:
                # Actualizar ficha existente
                ficha = service.actualizar_ficha_completa(ficha_id, datos_ficha, datos_examen)
                flash('Ficha clínica actualizada exitosamente', 'success')
            else:
                # Crear nueva ficha
                ficha = service.crear_ficha_completa(paciente_id, datos_ficha, datos_examen)
                flash('Ficha clínica creada exitosamente', 'success')
            
            return redirect(url_for('ficha_clinica.ver_ficha', ficha_id=ficha.id))
            
        except Exception as e:
            logger.error(f"Error en _procesar_formulario_ficha: {str(e)}")
            flash('Error al procesar la ficha clínica', 'error')
            raise
    
    @staticmethod
    def _extraer_datos_examen(form_data) -> Dict[str, Any]:
        """
        Extrae todos los datos del examen oftalmológico del formulario
        """
        # Lista de todos los campos del examen
        campos_examen = [
            # Agudeza Visual
            'av_distancia_od', 'av_distancia_oi', 'av_c_c_od', 'av_c_c_oi',
            'av_s_c_od', 'av_s_c_oi', 'av_ph_od', 'av_ph_oi',
            'av_proxima_od', 'av_proxima_oi', 'av_ao_distancia', 'av_ao_proxima',
            'dominante_od', 'dominante_oi', 'av_otros',
            
            # Lensometría
            'lensometria_od', 'lensometria_oi',
            
            # Queratometría
            'queratometria_od', 'queratometria_oi',
            
            # Autorefractor
            'ar_esf_od', 'ar_cyl_od', 'ar_eje_od', 'ar_av_od',
            'ar_esf_oi', 'ar_cyl_oi', 'ar_eje_oi', 'ar_av_oi',
            
            # Subjetivo
            'sub_esf_od', 'sub_cyl_od', 'sub_eje_od', 'sub_av_od',
            'sub_esf_oi', 'sub_cyl_oi', 'sub_eje_oi', 'sub_av_oi',
            
            # RX Final
            'rx_esf_od', 'rx_cyl_od', 'rx_eje_od', 'rx_avl_od', 'rx_avc_od',
            'rx_dp_od', 'rx_np_od', 'rx_add_od', 'rx_alt_od', 'rx_ao_od',
            'rx_esf_oi', 'rx_cyl_oi', 'rx_eje_oi', 'rx_avl_oi', 'rx_avc_oi',
            'rx_dp_oi', 'rx_np_oi', 'rx_add_oi', 'rx_alt_oi', 'rx_ao_oi',
            
            # Lentes de Contacto
            'lc_poder_od', 'lc_curva_base_od', 'lc_diametro_od', 'lc_adicion_od',
            'lc_diseno_od', 'lc_material_od', 'lc_poder_oi', 'lc_curva_base_oi',
            'lc_diametro_oi', 'lc_adicion_oi', 'lc_diseno_oi', 'lc_material_oi',
            
            # Test Adicionales
            'campimetria_t100_od', 'campimetria_n60_od', 'campimetria_s60_od', 'campimetria_i70_od',
            'campimetria_t100_oi', 'campimetria_n60_oi', 'campimetria_s60_oi', 'campimetria_i70_oi',
            'cover_test_pfc', 'cover_test_foria', 'cover_test_tropia', 'cover_test_mag_desviacion',
            'mov_oculares', 'luces_worth_lejos', 'luces_worth_cerca', 'test_ishihara',
            'presion_intraocular_od', 'presion_intraocular_oi', 'test_adicionales_otros',
            
            # Biomicroscopía
            'biomic_cornea_od', 'biomic_cornea_oi', 'biomic_cristalino_od', 'biomic_cristalino_oi',
            'biomic_pupila_od', 'biomic_pupila_oi', 'biomic_pestanas_od', 'biomic_pestanas_oi',
            'biomic_conjuntiva_bulbar_od', 'biomic_conjuntiva_bulbar_oi',
            'biomic_conjuntiva_tarsal_od', 'biomic_conjuntiva_tarsal_oi',
            'biomic_esclera_od', 'biomic_esclera_oi', 'biomic_pliegue_semilunar_od', 'biomic_pliegue_semilunar_oi',
            'biomic_caruncula_od', 'biomic_caruncula_oi', 'biomic_conductos_lagrimales_od', 'biomic_conductos_lagrimales_oi',
            'biomic_parpado_superior_od', 'biomic_parpado_superior_oi',
            'biomic_camara_anterior_od', 'biomic_camara_anterior_oi',
            'biomic_parpado_inferior_od', 'biomic_parpado_inferior_oi', 'biomic_otros',
            
            # Reflejos Pupilares
            'reflejo_acomodativo_miosis_od', 'reflejo_acomodativo_convergencia_od', 'reflejo_acomodativo_midriasis_od',
            'reflejo_acomodativo_miosis_oi', 'reflejo_acomodativo_convergencia_oi', 'reflejo_acomodativo_midriasis_oi',
            'reflejo_fotomotor_miosis_od', 'reflejo_fotomotor_midriasis_od', 'reflejo_consensual_od',
            'reflejo_fotomotor_miosis_oi', 'reflejo_fotomotor_midriasis_oi', 'reflejo_consensual_oi',
            
            # Fondo de Ojo
            'fondo_ojo_av_temp_sup_od', 'fondo_ojo_av_temp_inf_od', 'fondo_ojo_av_nasal_sup_od', 'fondo_ojo_av_nasal_inf_od',
            'fondo_ojo_retina_od', 'fondo_ojo_macula_od', 'fondo_ojo_excavacion_od', 'fondo_ojo_vasos_od',
            'fondo_ojo_papila_od', 'fondo_ojo_fijacion_od', 'fondo_ojo_color_od', 'fondo_ojo_borde_od',
            'fondo_ojo_av_temp_sup_oi', 'fondo_ojo_av_temp_inf_oi', 'fondo_ojo_av_nasal_sup_oi', 'fondo_ojo_av_nasal_inf_oi',
            'fondo_ojo_retina_oi', 'fondo_ojo_macula_oi', 'fondo_ojo_excavacion_oi', 'fondo_ojo_vasos_oi',
            'fondo_ojo_papila_oi', 'fondo_ojo_fijacion_oi', 'fondo_ojo_color_oi', 'fondo_ojo_borde_oi',
            'fondo_ojo_otros',
            
            # Otros Datos Médicos
            'glucosa', 'trigliceridos', 'atp', 'colesterol'
        ]
        
        datos_examen = {}
        
        for campo in campos_examen:
            valor = form_data.get(campo, '').strip()
            if valor:
                datos_examen[campo] = valor
        
        # Campos especiales (enteros)
        campos_enteros = ['hirschberg_od', 'hirschberg_oi', 'presion_arterial_sistolica', 
                         'presion_arterial_diastolica', 'saturacion_o2']
        
        for campo in campos_enteros:
            valor = form_data.get(campo, '').strip()
            if valor and valor.isdigit():
                datos_examen[campo] = int(valor)
        
        return datos_examen