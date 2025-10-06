from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import psycopg2
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'oftalmetryc-secret-key-2024'

# Configuración de BD
DB_CONFIG = {
    'host': 'localhost',
    'database': 'oftalmetryc_db', 
    'user': 'postgres',
    'password': '12345',
    'port': '5432'
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT u.usuario_id, u.nombre, r.nombre as rol
            FROM usuario u 
            JOIN rol r ON u.rol_id = r.rol_id
            WHERE u.username = %s AND u.password = %s AND u.estado = 'A'
        """, (username, password))
        
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['nombre'] = user[1]
            session['rol'] = user[2]
            flash(f'¡Bienvenido a Oftalmetryc, {user[1]}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Credenciales inválidas', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('login'))

@app.route('/productos')
def productos():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM producto WHERE estado = 'activo' ORDER BY nombre")
    productos = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('productos.html', productos=productos)

if __name__ == '__main__':
    print("🚀 Iniciando Oftalmetryc...")
    print("📱 Accede en: http://localhost:5000")
    print("👤 Usuario: admin")
    print("🔐 Contraseña: admin")
    app.run(debug=True, host='0.0.0.0', port=5000)