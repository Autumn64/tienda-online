CREATE DATABASE IF NOT EXISTS tienda_online_test;
USE tienda_online_test;

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
    
    nombre VARCHAR(30),
    precio DECIMAL(7,2),
    descripcion VARCHAR(255),
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

CREATE TABLE IF NOT EXISTS modificaciones(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    producto_id INTEGER NOT NULL,
    autor_id INTEGER NOT NULL,
    
    fecha_modificacion DATETIME,
    razon VARCHAR(255),
    
    CONSTRAINT FK_modificaciones_producto_id FOREIGN KEY (producto_id) REFERENCES productos(id),
    CONSTRAINT FK_modificaciones_autor_id FOREIGN KEY (autor_id) REFERENCES usuarios(id)
);

-- Categorías
CREATE TABLE IF NOT EXISTS categorias(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(30),
    descripcion VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS productos_categorias(
    producto_id INTEGER NOT NULL,
    categoria_id INTEGER NOT NULL,
    
    PRIMARY KEY (producto_id, categoria_id),
    CONSTRAINT FK_productos_categorias_producto_id FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE,
    CONSTRAINT FK_productos_categorias_categoria_id FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE CASCADE
);

-- Transacciones y compras
CREATE TABLE IF NOT EXISTS compras(
    id INTEGER PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    
    monto DECIMAL(10,2),
    fecha_creacion DATETIME,
    
    CONSTRAINT FK_compras_usuario_id FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS transacciones(
    id INTEGER PRIMARY KEY,
    producto_id INTEGER NOT NULL,
    compra_id INTEGER NOT NULL,
    
    cantidad INTEGER,
    
    CONSTRAINT FK_transacciones_producto_id FOREIGN KEY (producto_id) REFERENCES productos(id),
    CONSTRAINT FK_transacciones_compra_id FOREIGN KEY (compra_id) REFERENCES compras(id)
);