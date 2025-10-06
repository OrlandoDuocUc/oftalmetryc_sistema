#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GENERAR HASH VÁLIDO PARA CONTRASEÑA
================================
"""

from werkzeug.security import generate_password_hash

# Generar hash para la contraseña 'admin'
hash_valido = generate_password_hash("admin")
print("🔑 Hash válido para contraseña 'admin':")
print(hash_valido)
print("\n📋 Comando SQL para actualizar:")
print(f"UPDATE usuarios SET password = '{hash_valido}' WHERE username = 'admin';")