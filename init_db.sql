-- ============================================================
-- AURA SPA - Base de datos local
-- Ejecutar en MySQL con: source init_db.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS AURA_SPA
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE AURA_SPA;

-- Tabla reservas
CREATE TABLE IF NOT EXISTS reservas (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  codigo VARCHAR(255),
  nombre VARCHAR(255),
  email VARCHAR(255),
  telefono VARCHAR(50),
  servicio VARCHAR(100),
  especialista VARCHAR(100),
  fecha DATE,
  hora VARCHAR(20),
  mensaje TEXT,
  estado VARCHAR(50) DEFAULT 'pendiente',
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  actualizado_en TIMESTAMP NULL
);

-- Tabla servicios
CREATE TABLE IF NOT EXISTS servicios (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255),
  description TEXT,
  price DECIMAL(10,2),
  image_url VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  destacado BOOLEAN DEFAULT FALSE
);

-- Tabla usuarios
CREATE TABLE IF NOT EXISTS usuarios (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  rol VARCHAR(50) DEFAULT 'admin',
  creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- USUARIOS DE PRUEBA (contraseñas en texto plano para dev local)
-- El backend soporta tanto texto plano como bcrypt
-- ============================================================
INSERT INTO usuarios (email, password, rol, creado_en)
VALUES
  ('admin@spa.com', 'admin123', 'admin', NOW()),
  ('allison@gmail.com', 'allison2', 'admin', NOW())
ON DUPLICATE KEY UPDATE email = email;
