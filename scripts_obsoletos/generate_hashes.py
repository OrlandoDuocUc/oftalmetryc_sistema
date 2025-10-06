from werkzeug.security import generate_password_hash

# Mostrar hashes para inserción manual
admin_hash = generate_password_hash('admin')
orlando_hash = generate_password_hash('orlando')

print("=== HASHES PARA INSERCIÓN MANUAL ===")
print(f"admin: {admin_hash}")
print(f"orlando: {orlando_hash}")

print("\n=== COMANDOS SQL PARA COPIAR ===")
print(f"INSERT INTO usuario (nombre, ap_pat, ap_mat, username, email, password, estado, rol_id) VALUES ('Administrador', 'Sistema', '', 'admin', 'admin@oftalmetryc.com', '{admin_hash}', 'A', 1);")
print(f"INSERT INTO usuario (nombre, ap_pat, ap_mat, username, email, password, estado, rol_id) VALUES ('Orlando', 'Usuario', 'Vendedor', 'orlando', 'orlando@oftalmetryc.com', '{orlando_hash}', 'A', 2);")