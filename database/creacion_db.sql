CREATE DATABASE IF NOT EXISTS pupuseria;
USE pupuseria;

-- Tabla: ventas
CREATE TABLE IF NOT EXISTS ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) NOT NULL,
    pago DECIMAL(10,2) NOT NULL,
    cambio DECIMAL(10,2) NOT NULL
);

-- Tabla: productos
CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL
);

-- Insertar productos iniciales
INSERT INTO productos (nombre, precio) VALUES
('Pupusa de Queso', 1.00),
('Pupusa Revuelta', 1.25),
('Pupusa de Frijol', 1.00),
('Pollo en Pan', 3.50),
('Pollo con Papas', 4.50),
('Agua', 0.75),
('Jugo', 1.00),
('Cerveza', 2.00);

-- Tabla: detalle_venta (relación entre venta y productos)
CREATE TABLE IF NOT EXISTS detalle_venta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venta_id INT,
    producto_id INT,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (venta_id) REFERENCES ventas(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);