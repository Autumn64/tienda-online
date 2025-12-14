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