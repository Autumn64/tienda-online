DROP DATABASE IF EXISTS tienda_online;

CREATE DATABASE IF NOT EXISTS tienda_online;
USE tienda_online;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(30),
    email VARCHAR(100),
    passwd VARCHAR(255),
    tipo ENUM("cliente", "admin"),
    verificado BOOLEAN,
    eliminado BOOLEAN,
    fecha_creacion DATETIME
);

-- Manejo de productos
CREATE TABLE IF NOT EXISTS productos(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    autor_id INTEGER NOT NULL,
    
    nombre VARCHAR(255),
    precio DECIMAL(7,2),
    descripcion TEXT,
    stock INTEGER,
    fecha_creacion DATETIME,
    eliminado BOOLEAN,
    
    CONSTRAINT FK_productos_autor_id FOREIGN KEY (autor_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS imagenes(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    producto_id INTEGER NOT NULL,
    
    ruta VARCHAR(255),
    
    CONSTRAINT FK_imagenes_producto_id FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Transacciones y compras
CREATE TABLE IF NOT EXISTS compras(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    usuario_id INTEGER NOT NULL,
    
    monto DECIMAL(10,2),
    fecha_creacion DATETIME,
    
    CONSTRAINT FK_compras_usuario_id FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS transacciones(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    producto_id INTEGER NOT NULL,
    compra_id INTEGER NOT NULL,
    
    cantidad INTEGER,
    
    CONSTRAINT FK_transacciones_producto_id FOREIGN KEY (producto_id) REFERENCES productos(id),
    CONSTRAINT FK_transacciones_compra_id FOREIGN KEY (compra_id) REFERENCES compras(id)
);

-- Vista para las tarjetas de producto, que sólo recuperan la primera imagen.
CREATE OR REPLACE VIEW tarjetas_productos AS
SELECT 
    p.id,
    p.nombre,
    p.precio,
    i.ruta AS imagen
FROM productos p
LEFT JOIN imagenes i 
    ON i.id = (
        SELECT MIN(id)
        FROM imagenes
        WHERE producto_id = p.id
    )
WHERE 
    p.stock > 0
    AND p.eliminado = 0;

-- Vista para mostrar una compra con todos sus productos y cantidades.
CREATE OR REPLACE VIEW productos_compras AS
SELECT
    t.compra_id,
    p.nombre,
    p.precio,
    t.cantidad,
    i.ruta AS imagen
    FROM productos p
    INNER JOIN transacciones t
        ON p.id = t.producto_id
    LEFT JOIN imagenes i 
    ON i.id = (
        SELECT MIN(id)
        FROM imagenes
        WHERE producto_id = p.id
    );