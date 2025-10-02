#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Solución temporal: Crear un diagnóstico web que funcione sin problemas de codificación
"""

from flask import Flask, jsonify, render_template_string
import os
import sys

# Configurar encoding UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'

app = Flask(__name__)

@app.route('/test-consultas')
def test_consultas():
    """Ruta de prueba para verificar si las consultas funcionan"""
    
    # Datos de prueba simulados
    consultas_simuladas = [
        {
            'id': 1,
            'fecha_consulta': '2024-10-01T10:30:00',
            'paciente_nombre': 'Juan Pérez',
            'paciente_rut': '12.345.678-9',
            'medico': 'Dr. García',
            'motivo_consulta': 'Control de rutina - Examen visual',
            'estado': 'completada',
            'proxima_cita': '2024-11-01',
            'diagnostico': 'Miopía leve'
        },
        {
            'id': 2,
            'fecha_consulta': '2024-10-02T14:15:00',
            'paciente_nombre': 'María González',
            'paciente_rut': '98.765.432-1',
            'medico': 'Dr. López',
            'motivo_consulta': 'Molestias oculares y visión borrosa',
            'estado': 'activa',
            'proxima_cita': None,
            'diagnostico': 'Pendiente evaluación'
        },
        {
            'id': 3,
            'fecha_consulta': '2024-10-02T16:00:00',
            'paciente_nombre': 'Carlos Rodríguez',
            'paciente_rut': '11.222.333-4',
            'medico': 'Dr. García',
            'motivo_consulta': 'Seguimiento post-cirugía',
            'estado': 'activa',
            'proxima_cita': '2024-10-15',
            'diagnostico': 'Recuperación satisfactoria'
        }
    ]
    
    return jsonify({
        'success': True,
        'data': consultas_simuladas,
        'total': len(consultas_simuladas),
        'mensaje': 'Datos de prueba cargados correctamente',
        'problema_identificado': 'Error de codificación UTF-8 impide acceso a base de datos',
        'solucion': 'Usar datos simulados para verificar funcionamiento del frontend'
    })

@app.route('/diagnostico-consultas')
def diagnostico_consultas():
    """Página de diagnóstico del sistema de consultas"""
    
    html_template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Diagnóstico Sistema de Consultas</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            body { background-color: #f8f9fa; }
            .diagnostic-card { border-left: 4px solid #007bff; }
            .success-card { border-left: 4px solid #28a745; }
            .warning-card { border-left: 4px solid #ffc107; }
            .error-card { border-left: 4px solid #dc3545; }
        </style>
    </head>
    <body>
        <div class="container mt-4">
            <div class="row">
                <div class="col-12">
                    <h1 class="text-center mb-4">
                        <i class="fas fa-stethoscope me-2"></i>
                        Diagnóstico Sistema de Consultas Médicas
                    </h1>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-6 mb-4">
                    <div class="card error-card">
                        <div class="card-header bg-danger text-white">
                            <h5><i class="fas fa-exclamation-triangle me-2"></i>Problema Identificado</h5>
                        </div>
                        <div class="card-body">
                            <p><strong>Error UTF-8:</strong> "'utf-8' codec can't decode byte 0xf3 in position 85"</p>
                            <p><strong>Impacto:</strong> No se puede conectar a la base de datos PostgreSQL</p>
                            <p><strong>Síntoma:</strong> Las fichas clínicas no aparecen en el historial</p>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-6 mb-4">
                    <div class="card success-card">
                        <div class="card-header bg-success text-white">
                            <h5><i class="fas fa-check-circle me-2"></i>Arquitectura Correcta</h5>
                        </div>
                        <div class="card-body">
                            <p>✅ <strong>Controller:</strong> consulta_medica_controller.py</p>
                            <p>✅ <strong>Service:</strong> consulta_medica_service.py</p>
                            <p>✅ <strong>Repository:</strong> sql_consulta_medica_repository.py</p>
                            <p>✅ <strong>Frontend:</strong> consultas.html funcionando</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-12 mb-4">
                    <div class="card diagnostic-card">
                        <div class="card-header bg-primary text-white">
                            <h5><i class="fas fa-flask me-2"></i>Prueba de Funcionamiento</h5>
                        </div>
                        <div class="card-body">
                            <p>Clic en el botón para probar si el frontend funciona con datos simulados:</p>
                            <button class="btn btn-primary" onclick="probarConsultas()">
                                <i class="fas fa-play me-2"></i>Probar Carga de Consultas
                            </button>
                            <div id="resultados" class="mt-3"></div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-12 mb-4">
                    <div class="card warning-card">
                        <div class="card-header bg-warning">
                            <h5><i class="fas fa-tools me-2"></i>Soluciones Propuestas</h5>
                        </div>
                        <div class="card-body">
                            <ol>
                                <li><strong>Solución Inmediata:</strong> Corregir encoding en configuración de PostgreSQL</li>
                                <li><strong>Verificar:</strong> Variables de entorno y conexión a base de datos</li>
                                <li><strong>Alternativa:</strong> Reinstalar psycopg2 con configuración UTF-8</li>
                                <li><strong>Temporal:</strong> Usar datos simulados mientras se corrige el problema</li>
                            </ol>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="fas fa-chart-line me-2"></i>Estado del Sistema</h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-3 text-center">
                                    <div class="text-success">
                                        <i class="fas fa-code fa-2x"></i>
                                        <p class="mt-2"><strong>Frontend</strong><br>Funcionando</p>
                                    </div>
                                </div>
                                <div class="col-md-3 text-center">
                                    <div class="text-success">
                                        <i class="fas fa-cogs fa-2x"></i>
                                        <p class="mt-2"><strong>Backend</strong><br>Funcionando</p>
                                    </div>
                                </div>
                                <div class="col-md-3 text-center">
                                    <div class="text-danger">
                                        <i class="fas fa-database fa-2x"></i>
                                        <p class="mt-2"><strong>Base de Datos</strong><br>Error Codificación</p>
                                    </div>
                                </div>
                                <div class="col-md-3 text-center">
                                    <div class="text-warning">
                                        <i class="fas fa-eye fa-2x"></i>
                                        <p class="mt-2"><strong>Fichas Clínicas</strong><br>No Visibles</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            async function probarConsultas() {
                const resultadosDiv = document.getElementById('resultados');
                resultadosDiv.innerHTML = '<div class="spinner-border text-primary" role="status"></div> Cargando...';
                
                try {
                    const response = await fetch('/test-consultas');
                    const data = await response.json();
                    
                    if (data.success) {
                        resultadosDiv.innerHTML = `
                            <div class="alert alert-success">
                                <h6><i class="fas fa-check me-2"></i>Prueba Exitosa</h6>
                                <p><strong>Consultas cargadas:</strong> ${data.total}</p>
                                <p><strong>Mensaje:</strong> ${data.mensaje}</p>
                                <details>
                                    <summary>Ver datos de ejemplo</summary>
                                    <pre class="mt-2">${JSON.stringify(data.data, null, 2)}</pre>
                                </details>
                            </div>
                        `;
                    } else {
                        resultadosDiv.innerHTML = `
                            <div class="alert alert-danger">
                                <h6><i class="fas fa-times me-2"></i>Error en la Prueba</h6>
                                <p>No se pudieron cargar las consultas simuladas</p>
                            </div>
                        `;
                    }
                } catch (error) {
                    resultadosDiv.innerHTML = `
                        <div class="alert alert-danger">
                            <h6><i class="fas fa-times me-2"></i>Error de Conexión</h6>
                            <p>${error.message}</p>
                        </div>
                    `;
                }
            }
        </script>
    </body>
    </html>
    """
    
    return render_template_string(html_template)

if __name__ == '__main__':
    print("🏥 Servidor de Diagnóstico de Consultas Médicas")
    print("=" * 50)
    print("📊 Diagnóstico disponible en: http://localhost:5001/diagnostico-consultas")
    print("🧪 API de prueba en: http://localhost:5001/test-consultas")
    print("💡 Usa Ctrl+C para detener el servidor")
    print()
    
    app.run(debug=True, port=5001, host='0.0.0.0')