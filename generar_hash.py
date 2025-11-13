"""
Script temporal para generar el hash correcto de la contraseña admin123
usando la misma función que usa tu aplicación Flask.
"""
from werkzeug.security import generate_password_hash

# Generar el hash para 'admin123'
password = 'admin123'
hash_generado = generate_password_hash(password)

print("=" * 80)
print("HASH GENERADO PARA LA CONTRASEÑA: admin123")
print("=" * 80)
print(hash_generado)
print("=" * 80)
print("\nEjecuta este comando en psql:")
print(f"UPDATE usuarios SET password = '{hash_generado}' WHERE username = 'admin';")
print("=" * 80)
