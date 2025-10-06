-- Script para crear usuarios con hashes werkzeug correctos
-- Ejecutar en DBeaver o cliente PostgreSQL

-- Limpiar usuarios existentes (opcional)
DELETE FROM usuario;

-- Insertar usuario admin
INSERT INTO usuario (nombre, ap_pat, ap_mat, username, email, password, estado, rol_id) 
VALUES ('Administrador', 'Sistema', '', 'admin', 'admin@oftalmetryc.com', 'scrypt:32768:8:1$YNx7QtiZ2BTdqWeB$56f458904cb782fd026c1b4f11fe75c59c9b2e92b48fd0e09f084d29add66d3362a3b2adfdbce70e41f2df68377128072031785b0ff1201ac51040cf1da9b4f4', 'A', 1);

-- Insertar usuario orlando
INSERT INTO usuario (nombre, ap_pat, ap_mat, username, email, password, estado, rol_id) 
VALUES ('Orlando', 'Usuario', 'Vendedor', 'orlando', 'orlando@oftalmetryc.com', 'scrypt:32768:8:1$nkA90b86YTTTtLjT$d3fe47fe13d965d07bfb90a885b86cb02149a10b24b7eb012b01f07d4abdf33e3d0e839f06badf78bd4dc6f10c06e3507a8d3d5b420eafa9dc024ecec9d92693', 'A', 2);

-- Verificar usuarios creados
SELECT usuario_id, nombre, username, email, estado, rol_id FROM usuario;